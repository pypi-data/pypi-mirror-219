
use prompt_graph_core::create_change_value;
use prompt_graph_core::proto2::{ChangeValueWithCounter, InputProposal, ItemCore, PromptGraphConstant, PromptGraphNodeComponent, PromptGraphNodeMemory, PromptGraphNodeObservation, PromptGraphParameterNode};
use prompt_graph_core::proto2::prompt_graph_node_component::Transclusion;

pub fn node_parameter_init(n: &PromptGraphParameterNode, core: &ItemCore, branch: u64, counter: u64) -> (Vec<ChangeValueWithCounter>, Vec<InputProposal>) {
    // output type definitions indicate the expected structure of these inputs
    (vec![], vec![InputProposal {
        name: core.name.clone(),
        output: core.output.clone(),
        branch,
        counter
    }])
}

pub fn node_observation_init(n: &PromptGraphNodeObservation, core: &ItemCore, branch: u64, counter: u64) -> (Vec<ChangeValueWithCounter>, Vec<InputProposal>) {
    (vec![], vec![InputProposal {
        name: core.name.clone(),
        output: core.output.clone(),
        branch,
        counter
    }])
}

pub fn node_constant_init(c: &PromptGraphConstant, core: &ItemCore, branch: u64, counter: u64) -> (Vec<ChangeValueWithCounter>, Vec<InputProposal>) {
    (vec![ChangeValueWithCounter {
        source_node: "constant".to_string(),
        filled_values: vec![
            create_change_value(
                vec![core.name.clone()],
                c.value.as_ref().unwrap().val.clone(),
            branch)
        ],
        parent_monotonic_counters: vec![],
        monotonic_counter: counter,
        branch,
    }], vec![])
}

pub fn node_component_init(n: &PromptGraphNodeComponent, core: &ItemCore, branch: u64, counter: u64) -> (Vec<ChangeValueWithCounter>, Vec<InputProposal>) {
    unimplemented!();
    if let Some(transclusion) = &n.transclusion {
        match transclusion {
            Transclusion::InlineFile(f) => {
                // Kick off another process to handle this
            }
            Transclusion::BytesReference(_) => {
                // Deserialize and kick off
            }
            Transclusion::S3PathReference(_) => {
                // Download and kick off
            }
            _ => {}
        }
    }
    (vec![], vec![])
}
