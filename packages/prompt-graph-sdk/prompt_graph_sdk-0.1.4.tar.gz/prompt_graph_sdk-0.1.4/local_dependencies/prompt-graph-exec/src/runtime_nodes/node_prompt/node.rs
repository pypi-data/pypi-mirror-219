use std::collections::HashSet;
use std::env;
use prompt_graph_core::proto2::{ChangeValue, ItemCore, NodeWillExecute, PromptGraphNodePrompt, SupportedChatModel};
use prompt_graph_core::proto2::serialized_value::Val;
use prompt_graph_core::templates::render_template_prompt;
use futures::executor;
use prompt_graph_core::proto2::prompt_graph_node_prompt::Model;
use crate::integrations::openai::batch::chat_completion;

pub async fn execute_node_prompt(node_will_execute: &NodeWillExecute, n: &&PromptGraphNodePrompt, core: &ItemCore, namespaces: &HashSet<String>) -> Vec<ChangeValue> {
    let mut change_set = &node_will_execute
        .change_values_used_in_execution.iter().filter_map(|x| x.change_value.as_ref().cloned());
    let mut filled_values = vec![];
    // n.model;
    // n.frequency_penalty;
    // n.max_tokens;
    // n.presence_penalty;
    // n.stop;
    if let Some(Model::ChatModel(model)) = n.model {
        let m = SupportedChatModel::from_i32(model).unwrap();
        let templated_string = render_template_prompt(&n.template, &change_set.clone().collect()).unwrap();
        let result = chat_completion(m, templated_string).await;
        for output_table in namespaces.iter() {
            filled_values.push(prompt_graph_core::create_change_value(
                vec![output_table.clone(), String::from("promptResult")],
                Some(Val::String(result.choices.first().unwrap().message.content.clone())),
                0)
            );
        }
    }
    filled_values
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_exec_node_prompt() {
    }
}
