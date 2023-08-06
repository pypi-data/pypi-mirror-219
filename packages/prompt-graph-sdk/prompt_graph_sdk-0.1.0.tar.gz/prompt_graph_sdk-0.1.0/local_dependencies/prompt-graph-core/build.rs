fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("cargo:rerun-if-changed=../../protobufs/DSL_v1.proto");
    tonic_build::compile_protos("../../protobufs/DSL_v1.proto")?;
    Ok(())
}