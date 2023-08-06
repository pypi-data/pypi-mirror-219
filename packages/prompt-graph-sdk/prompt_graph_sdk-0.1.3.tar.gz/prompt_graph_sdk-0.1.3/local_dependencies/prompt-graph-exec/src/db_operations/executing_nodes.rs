use crate::db_operations;
use crate::db_operations::{WILL_EXEC_COMPLETE_PREFIX, WILL_EXEC_IN_PROGRESS_PREFIX, WILL_EXEC_PENDING_PREFIX};
use prost::Message;
use sled::{Event, Subscriber};
use prompt_graph_core::proto2::NodeWillExecuteOnBranch;


// TODO: remove node name from all of these

/// This stores logs of EventExecutionGraphExecutingNode records, denoting the input and output
/// keys of a node's execution.
pub fn will_exec_pending_custom_node_prefix() -> Vec<u8> {
    db_operations::encode_into_slice((WILL_EXEC_PENDING_PREFIX, true)).unwrap()
}

pub fn will_exec_pending_prefix(is_custom_node: bool, branch: u64, counter: u64) -> Vec<u8> {
    db_operations::encode_into_slice((WILL_EXEC_PENDING_PREFIX, is_custom_node, branch, counter)).unwrap()
}

pub fn will_exec_in_progress_prefix( is_custom_node: bool, branch: u64, counter: u64) -> Vec<u8> {
    db_operations::encode_into_slice((WILL_EXEC_IN_PROGRESS_PREFIX, is_custom_node, branch, counter, )).unwrap()
}

pub fn will_exec_complete_prefix(is_custom_node: bool, branch: u64, counter: u64) -> Vec<u8> {
    db_operations::encode_into_slice((WILL_EXEC_COMPLETE_PREFIX, is_custom_node, branch, counter)).unwrap()
}

pub fn will_exec_pending_prefix_raw() -> Vec<u8> {
    db_operations::encode_into_slice((WILL_EXEC_PENDING_PREFIX)).unwrap()
}

// =================
// Handling capturing and communicating nodes that are currently processing
pub fn insert_will_execute(tree: &sled::Tree, will_exec: NodeWillExecuteOnBranch) {
    let NodeWillExecuteOnBranch { custom_node_type_name, node, branch, counter } = &will_exec;
    let node = node.as_ref().unwrap();
    let is_custom_node = custom_node_type_name.is_some();
    tree.insert(will_exec_pending_prefix(is_custom_node, *branch, *counter), will_exec.encode_to_vec()).unwrap();
}

pub fn scan_all_will_execute_events(tree: &sled::Tree) -> impl Iterator<Item = NodeWillExecuteOnBranch> {
    tree.scan_prefix(will_exec_pending_prefix_raw())
        .map(|c| NodeWillExecuteOnBranch::decode(c.unwrap().1.as_ref()).unwrap())
}

pub fn scan_all_custom_node_will_execute_events(tree: &sled::Tree) -> impl Iterator<Item = NodeWillExecuteOnBranch> {
    tree.scan_prefix(will_exec_pending_custom_node_prefix())
        .map(|c| NodeWillExecuteOnBranch::decode(c.unwrap().1.as_ref()).unwrap())
}

pub fn move_will_execute_event_to_in_progress(tree: &sled::Tree, is_custom_node: bool, branch: u64, counter: u64) {
    // Handle not found to remove in order to allow receiving multiple identical messages
    if let Some(prev) = tree.remove(will_exec_pending_prefix( is_custom_node, branch, counter)).unwrap() {
        tree.insert(will_exec_in_progress_prefix(is_custom_node,  branch, counter), prev).unwrap();
    }
}

pub fn move_will_execute_event_to_complete(tree: &sled::Tree, is_custom_node: bool, branch: u64, counter: u64) {
    let prev = tree.remove(will_exec_in_progress_prefix(is_custom_node,  branch, counter)).unwrap().expect("Changes must exist to be resolved");
    tree.insert(will_exec_complete_prefix(is_custom_node,  branch, counter), prev).unwrap();
}

pub fn subscribe_to_will_execute_events(tree: &sled::Tree) -> sled::Subscriber {
    tree.watch_prefix(will_exec_pending_prefix_raw())
}

pub fn subscribe_to_will_execute_events_by_name(tree: &sled::Tree) -> Subscriber {
    tree.watch_prefix(will_exec_pending_prefix_raw())
}
