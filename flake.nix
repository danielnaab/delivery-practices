{
  description = "delivery-practices: knowledge base for software delivery practices enabling fast and safe AI-assisted development";
  inputs.self.submodules = true;
  inputs.graft.url = "github:danielnaab/graft/v2.13.1";
  outputs = inputs: inputs.graft.lib.mkFlake { inherit inputs; };
}
