use serde::{de, Deserialize, Deserializer, Serialize, Serializer};
use serde::de::{Error, Visitor};
use std::fmt;
use prost::Message;
use crate::proto2::File;

impl Serialize for File {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
        where
            S: Serializer,
    {
        let mut buffer = Vec::new();
        &self.encode(&mut buffer).unwrap();
        serializer.serialize_bytes(&buffer)
    }
}

struct FileVisitor;

impl<'de> Visitor<'de> for FileVisitor {
    type Value = File;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("struct File")
    }

    fn visit_bytes<E>(self, value: &[u8]) -> Result<File, E>
        where
            E: de::Error,
    {
        File::decode(value).map_err(|e| E::custom(format!("{}", e)))
    }
}

impl<'de> Deserialize<'de> for File {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
        where
            D: Deserializer<'de>,
    {
        deserializer.deserialize_bytes(FileVisitor)
    }
}
