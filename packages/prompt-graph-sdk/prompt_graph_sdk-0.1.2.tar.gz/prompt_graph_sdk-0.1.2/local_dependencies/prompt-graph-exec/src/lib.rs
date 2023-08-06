mod executor;
mod integrations;
mod runtime_nodes;
mod initialize_nodes;
pub mod tonic_runtime;
mod db_operations;

use neon::prelude::*;

use std::sync::mpsc;
use std::thread;

use neon::{prelude::*, types::Deferred};

#[macro_use]
extern crate lazy_static;

type DbCallback = Box<dyn FnOnce(&mut String, &Channel, Deferred) + Send>;

struct ExecutorGRPCServer {
    tx: mpsc::Sender<GRPCServerMessage>,
}

// Messages sent on the server channel
enum GRPCServerMessage {
    // Promise to resolve and callback to be executed
    // Deferred is threaded through the message instead of moved to the closure so that it
    // can be manually rejected.
    Callback(Deferred, DbCallback),
    // Indicates that the thread should be stopped and connection closed
    Close,
}

// Clean-up when Database is garbage collected, could go here
// but, it's not needed,
impl Finalize for ExecutorGRPCServer {}

// Internal implementation
impl ExecutorGRPCServer {
    fn new<'a, C>(port: String, mut cx: &mut C) -> Result<Self, String> where C: Context<'a>, {
        let (tx, rx) = mpsc::channel::<GRPCServerMessage>();
        let channel = cx.channel();
        thread::spawn(move || {
            tonic_runtime::run_server(port);
            while let Ok(message) = rx.recv() {
                match message {
                    GRPCServerMessage::Callback(deferred, f) => {
                    }
                    GRPCServerMessage::Close => break,
                }
            }
        });
        Ok(Self { tx })
    }

    // Idiomatic rust would take an owned `self` to prevent use after close
    // However, it's not possible to prevent JavaScript from continuing to hold a closed database
    fn close(&self) -> Result<(), mpsc::SendError<GRPCServerMessage>> {
        self.tx.send(GRPCServerMessage::Close)
    }

    fn send(
        &self,
        deferred: Deferred,
        callback: impl FnOnce(&mut String, &Channel, Deferred) + Send + 'static,
    ) -> Result<(), mpsc::SendError<GRPCServerMessage>> {
        self.tx
            .send(GRPCServerMessage::Callback(deferred, Box::new(callback)))
    }
}

impl ExecutorGRPCServer {
    fn js_new(mut cx: FunctionContext) -> JsResult<JsBox<ExecutorGRPCServer>> {
        let port = cx.argument::<JsString>(0)?.value(&mut cx);
        let db = ExecutorGRPCServer::new(port, &mut cx).or_else(|err| cx.throw_error(err.to_string()))?;
        Ok(cx.boxed(db))
    }

    fn js_close(mut cx: FunctionContext) -> JsResult<JsUndefined> {
        cx.this()
            .downcast_or_throw::<JsBox<ExecutorGRPCServer>, _>(&mut cx)?
            .close()
            .or_else(|err| cx.throw_error(err.to_string()))?;
        Ok(cx.undefined())
    }

    fn js_insert(mut cx: FunctionContext) -> JsResult<JsPromise> {
        let name = cx.argument::<JsString>(0)?.value(&mut cx);
        let db = cx.this().downcast_or_throw::<JsBox<ExecutorGRPCServer>, _>(&mut cx)?;
        let (deferred, promise) = cx.promise();
        db.send(deferred, move |conn, channel, deferred| {
            deferred.settle_with(channel, move |mut cx| {
                Ok(cx.number(0.0 as f64))
            });
        })
            .into_rejection(&mut cx)?;

        // This function does not have a return value
        Ok(promise)
    }
}

trait SendResultExt {
    fn into_rejection<'a, C: Context<'a>>(self, cx: &mut C) -> NeonResult<()>;
}

impl SendResultExt for Result<(), mpsc::SendError<GRPCServerMessage>> {
    fn into_rejection<'a, C: Context<'a>>(self, cx: &mut C) -> NeonResult<()> {
        self.or_else(|err| {
            let msg = err.to_string();
            match err.0 {
                GRPCServerMessage::Callback(deferred, _) => {
                    let err = cx.error(msg)?;
                    deferred.reject(cx, err);
                    Ok(())
                }
                GRPCServerMessage::Close => cx.throw_error("Expected DbMessage::Callback"),
            }
        })
    }
}

fn neon_start_server(mut cx: FunctionContext) -> JsResult<JsNumber> {
    let port = cx.argument::<JsString>(0)?.value(&mut cx);
    std::thread::spawn(|| {
        tonic_runtime::run_server(port);
    });
    Ok(cx.number(1.0 as f64))
}

#[neon::main]
fn neon_main(mut cx: ModuleContext) -> NeonResult<()> {
    cx.export_function("serverNew", ExecutorGRPCServer::js_new)?;
    cx.export_function("serverClose", ExecutorGRPCServer::js_close)?;
    cx.export_function("serverInsert", ExecutorGRPCServer::js_insert)?;
    cx.export_function("startServer", neon_start_server)?;
    Ok(())
}
