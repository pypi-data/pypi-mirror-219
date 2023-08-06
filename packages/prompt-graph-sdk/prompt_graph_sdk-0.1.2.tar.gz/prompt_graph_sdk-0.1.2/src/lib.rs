extern crate protobuf;
mod translations;
use serde::{Deserialize, Deserializer, Serialize, Serializer};
use prompt_graph_core::proto2::{Item, ChangeValue, ChangeValueWithCounter, File, OutputType, Path, PromptGraphNodeMemory, Query, SerializedValue};
use prompt_graph_core::proto2::serialized_value::Val;


// let mut compiler = ApolloCompiler::new();
// compiler.add_type_system(input, name);
//
// // TODO: capture these diagnostics and return them
// let diagnostics = compiler.validate();
// for diagnostic in &diagnostics {
//     // this will pretty-print diagnostics using the miette crate.
//     println!("{}", diagnostic);
// }


// if let Some(selection_set) = op_def.selection_set() {
//     print_field_names(None, selection_set);
// }
// let variable_defs = op_def.variable_definitions();
// let variables: Vec<String> = variable_defs
//     .iter()
//     .map(|v| v.variable_definitions())
//     .flatten()
//     .filter_map(|v| Some(v.variable()?.text().to_string()))
//     .collect();
// println!("{:?}", variables.as_slice());

// #[wasm_bindgen]
// fn pipeline(graph: DefinitionGraph) -> (DefinitionGraph, String) {
//     let type_docs = graph_parse::extract_output_types(&graph);
//     let mut compiler = ApolloCompiler::new();
//     let unified = graph_validate::build_type_document(&mut compiler, type_docs);
//     graph_validate::validate_query_types(&mut compiler, &graph);
//     // TODO: so at this point we now have the paths
//     (graph, unified.to_string())
// }

#[cfg(test)]
mod tests {

    use indoc::indoc;
    use crate::build_runtime_graph::graph_parse::{parse_graphql_type_def, parse_where_query};
    use crate::proto2::item::Item;

    #[test]
    fn test_parse_where_query() {
        parse_where_query("WHERE x = 1");
    }

    #[test]
    fn test_parse_graphql_type_def() {
        parse_graphql_type_def("ProductDimension", indoc! { r#"
        type ProductDimension {
          size: String
          weight: Float
        }
        "#});
    }

    #[test]
    fn test_parse_graphql_type_def_rename() {
        assert_eq!(parse_graphql_type_def("OtherName", indoc! { r#"
        type ProductDimension {
          size: String
          weight: Float
        }
        "# }).unwrap().to_string(), indoc! { r#"
        type OtherName {
          size: String
          weight: Float
        }
        "# }
        );
    }

    #[test]
    fn test_capture_resources_referred_in_graphql() {
        // capture_resources_referred_in_graphql(indoc! { r#"
        //   query GraphQuery($graph_id: ID!, $variant: String) {
        //     service(id: $graph_id) {
        //       other(filter: "example query", another: 1) {
        //         otherValue
        //       }
        //       schema(tag: $variant) {
        //         document
        //       }
        //     }
        //   }
        // "# });
    }
}


/// Our local server implementation is an extension of this. Implementing support for multiple
/// agent implementations to run on the same machine.
pub fn create_change_value(address: Vec<String>, val: Option<Val>, branch: u64) -> ChangeValue {
    ChangeValue{
        path: Some(Path {
            address,
        }),
        value: Some(SerializedValue {
            val,
        }),
        branch,
    }
}
