use std::collections::HashSet;
use prompt_graph_core::proto2::{ChangeValue, ItemCore, NodeWillExecute, PromptGraphNodeCode, PromptGraphNodeCodeSourceCode, SupportedSourceCodeLanguages};
use prompt_graph_core::proto2::prompt_graph_node_code::Source;
use prompt_graph_core::templates::{flatten_value_keys, json_value_to_serialized_value};
use crate::runtime_nodes::node_code;
use deno_core::serde_json::Value;
use log::debug;

// TODO: need a function that recursively traverses object values




#[cfg(feature = "starlark")]
pub fn run_starlark(c: &PromptGraphNodeCodeSourceCode, change_set: &Vec<ChangeValue>) -> Option<Value> {
    node_code::starlark::source_code_run_starlark(c, change_set)
}

#[cfg(not(feature = "starlark"))]
pub fn run_starlark(c: &PromptGraphNodeCodeSourceCode, change_set: &Vec<ChangeValue>) -> Option<Value> {
    None
}


pub fn execute_node_code(node_will_execute: &NodeWillExecute, n: &PromptGraphNodeCode, core: &ItemCore, namespaces: &HashSet<String>) -> Vec<ChangeValue> {
    let mut change_set = &node_will_execute
        .change_values_used_in_execution.iter().filter_map(|x| x.change_value.clone());

    debug!("execute_node_code {:?}", &n);
    let mut filled_values = vec![];
    if let Some(source) = &n.source {
        match source {
            Source::SourceCode(c) => {
                let result = match SupportedSourceCodeLanguages::from_i32(c.language).unwrap() {
                    SupportedSourceCodeLanguages::Deno => {
                        node_code::deno::source_code_run_deno(c, &change_set.clone().collect())
                    },
                    SupportedSourceCodeLanguages::Starlark => {
                        run_starlark(c, &change_set.clone().collect())
                    }
                };
                let sresult = result.as_ref().map(json_value_to_serialized_value);
                if let Some(val) = sresult {
                    let flattened = flatten_value_keys(val, vec![]);
                    for (k, v) in flattened {
                        for output_table in namespaces.iter() {
                            let mut address = vec![output_table.clone()];
                            address.extend(k.clone());
                            filled_values.push(prompt_graph_core::create_change_value(
                                address,
                                Some(v.clone()),
                                0)
                            );
                        }
                    }
                }
            }
            Source::Zipfile(_) | Source::S3Path(_) => {
                unimplemented!("invoke docker container is not yet implemented");
            }
            _ => {}
        }
    }
    filled_values
}
