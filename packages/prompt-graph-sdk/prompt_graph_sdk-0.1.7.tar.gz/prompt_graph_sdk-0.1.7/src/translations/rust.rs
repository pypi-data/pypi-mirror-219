use prompt_graph_core::graph_definition::{
    create_prompt_node,
    create_op_map,
    create_code_node,
    create_component_node,
    create_vector_memory_node,
    create_observation_node,
    create_node_parameter
};
use anyhow::Result;
use prompt_graph_core::graph_definition::SourceNodeType;
use prompt_graph_core::graph_definition::DefinitionGraph;
use prompt_graph_core::build_runtime_graph::graph_parse::CleanedDefinitionGraph;
use prompt_graph_core::proto2::execution_runtime_client::ExecutionRuntimeClient;
use prompt_graph_core::proto2::RequestFileMerge;


// TODO: need to define pattern for automatically wiring dependencies
// TODO: add methods
// create_entrypoint_query

pub fn new_graph() -> DefinitionGraph {
    DefinitionGraph::zero()
}

#[macro_export]
macro_rules! register_all {
    ($graph:expr, $($statement:expr,)*) => {
        $( $graph.register_node($statement); )*
    };
}

#[macro_export]
macro_rules! parameter {
    ($output_def:expr) => {
        create_node_parameter(
            format!("{}:{}", file!(), line!()),
            String::from($output_def)
        )
    };
    ($name:expr, $output_def:expr) => {
        create_node_parameter(
            String::from($name),
            String::from($output_def)
        )
    };
}

#[macro_export]
macro_rules! map {
    ($query_def:expr, $path:expr) => {
        create_op_map(
            format!("{}:{}", file!(), line!()),
            String::from($query_def),
            String::from($path),
        )
    };
    ($name:expr, $query_def:expr, $path:expr) => {
        create_code_node(
            String::from($name),
            String::from($query_def),
            String::from($path),
        )
    };
}


#[macro_export]
macro_rules! code_node {
    ($query_def:expr, $output_def:expr, $source_type:expr) => {
        create_code_node(
            format!("{}:{}", file!(), line!()),
            String::from($query_def),
            String::from($output_def),
            $source_type,
        )
    };
    ($name:expr, $query_def:expr, $output_def:expr, $source_type:expr) => {
        create_code_node(
            String::from($name),
            String::from($query_def),
            String::from($output_def),
            String::from($source_type),
        )
    };
}


#[macro_export]
macro_rules! observation_node {
    ($query_def:expr, $output_def:expr) => {
        create_observation_node(
            format!("{}:{}", file!(), line!()),
            String::from($query_def),
            String::from($output_def),
        )
    };
    ($name:expr, $query_def:expr, $output_def:expr) => {
        create_observation_node(
            String::from($name),
            String::from($query_def),
            String::from($output_def),
        )
    };
}


#[macro_export]
macro_rules! memory_node {
    ($query_def:expr, $output_def:expr, $model:expr, $db:expr) => {
        create_vector_memory_node(
            format!("{}:{}", file!(), line!()),
            String::from($query_def),
            String::from($output_def),
            String::from($model),
            String::from($db)
        )
    };
    ($name:expr, $query_def:expr, $output_def:expr, $model:expr, $db:expr) => {
        create_vector_memory_node(
            String::from($name),
            String::from($query_def),
            String::from($output_def),
            String::from($model),
            String::from($db)
        )
    };
}

#[macro_export]
macro_rules! component_node {
    ($query_def:expr, $output_def:expr) => {
        create_component_node(
            format!("{}:{}", file!(), line!()),
            String::from($query_def),
            String::from($output_def),
        )
    };
    ($name:expr, $query_def:expr, $output_def:expr) => {
        create_component_node(
            String::from($name),
            String::from($query_def),
            String::from($output_def),
        )
    };
}

#[macro_export]
macro_rules! prompt_node {
    ($query_def:expr, $template:expr, $model:expr) => {
        create_prompt_node(
            format!("{}:{}", file!(), line!()),
            String::from($query_def),
            String::from($template),
            String::from($model),
        )
    };
    ($name:expr, $query_def:expr, $template:expr, $model:expr) => {
        create_prompt_node(
            String::from($name),
            String::from($query_def),
            String::from($template),
            String::from($model),
        )
    };
}

// TODO: local configuration
pub async fn run_worker(url: String, graph: DefinitionGraph) -> Result<()> {
    // validate the graph
    CleanedDefinitionGraph::new(&graph);
    let file_merge = RequestFileMerge{ file: Some(graph.get_file().clone()), branch: 0, id: "".to_string() };
    let mut client = ExecutionRuntimeClient::connect(url).await?;
    let _response = client.merge(file_merge).await?.into_inner();
    println!("after start client");
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::new_graph;

    #[test]
    fn test_new_graph() {
        new_graph();
    }
}
