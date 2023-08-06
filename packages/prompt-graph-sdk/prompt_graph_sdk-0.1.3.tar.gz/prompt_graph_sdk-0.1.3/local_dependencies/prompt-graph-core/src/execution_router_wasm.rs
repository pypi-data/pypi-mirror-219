use std::collections::HashMap;
use prost::Message;
use crate::execution_router;
use crate::execution_router::{ExecutionState};
use crate::graph_definition::DefinitionGraph;
use crate::build_runtime_graph::graph_parse::CleanedDefinitionGraph;
use crate::proto2::{ChangeValue, ChangeValueWithCounter};
use std::ops::Add;


#[derive(Debug)]
pub struct WasmState {
    value: HashMap<Vec<u8>, (u64, ChangeValue)>,
    node_executions: HashMap<Vec<u8>, u64>
}
impl WasmState {
    fn new() -> Self {
        Self {
            value: HashMap::new(),
            node_executions: HashMap::new()
        }
    }
}

impl ExecutionState for WasmState {
    fn inc_counter_node_execution(&mut self, node: &[u8]) -> u64 {
        self.node_executions.entry(node.to_vec()).or_insert(0).add(1)
    }

    fn get_count_node_execution(&self, node: &[u8]) -> Option<u64> {
        self.node_executions.get(node).map(|x| *x)
    }

    fn get_value(&self, address: &[u8]) -> Option<(u64, ChangeValue)> {
        self.value.get(address).cloned()
    }

    fn set_value(&mut self, address: &[u8], counter: u64, value: ChangeValue) {
        self.value.insert(address.to_vec(), (counter, value));
    }
}

// TODO: execution router should include a session token that is used to identify the session
// TODO: execution router should include a counter that represents what it has seen up until
pub struct ExecutionRouter {
    clean_definition_graph: CleanedDefinitionGraph,
    state: WasmState
}

impl ExecutionRouter {
    pub fn new(definition_graph: &DefinitionGraph) -> Self {
        let clean_definition_graph = CleanedDefinitionGraph::new(definition_graph);
        Self {
            clean_definition_graph,
            state: WasmState::new()
        }
    }


    /// This method accepts and encoded ChangeValueWithCounter and returns an encoded DispatchResult
    /// in order to support the wasm interface.
    pub fn dispatch_wasm(
        &mut self,
        bytes: &[u8],
    ) -> Vec<u8> {
        let change = ChangeValueWithCounter::decode(bytes).unwrap();

        let dispatch_result = execution_router::dispatch_and_mutate_state(
            &self.clean_definition_graph,
            &mut self.state,
            &change);

        // we only _tell_ what we think should happen. We don't actually do it.
        // it is up to the wrapping SDK what to do or not do with our information
        let mut buffer = Vec::new();
        dispatch_result.encode(&mut buffer).unwrap();
        buffer
    }
}
