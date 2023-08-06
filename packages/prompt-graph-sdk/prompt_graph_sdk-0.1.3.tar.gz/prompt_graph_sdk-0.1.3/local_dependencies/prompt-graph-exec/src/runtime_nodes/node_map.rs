use std::collections::HashSet;
use prompt_graph_core::proto2::{ChangeValue, NodeWillExecute, PromptGraphMap};
use prompt_graph_core::proto2::serialized_value::Val;

pub fn execute_node_map(node_will_execute: &NodeWillExecute, n: &PromptGraphMap, _: &HashSet<String>) -> Vec<ChangeValue> {
    let mut change_set: Vec<ChangeValue> = node_will_execute
        .change_values_used_in_execution.iter().filter_map(|x| x.change_value.clone()).collect();
    let mut filled_values = vec![];
    if let Some(change) = change_set.iter().find(|change| change.path.as_ref().unwrap().address.join(".") == n.path) {
        if let Val::Array(vec) = change.value.as_ref().unwrap().val.clone().unwrap() {
            for (i, item) in vec.values.iter().enumerate() {
                filled_values.push(prompt_graph_core::create_change_value(
                    vec![i.to_string()],
                    item.val.clone(),
                0));
            }
        }
    }
    filled_values
}
