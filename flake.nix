{
  description = "delivery-practices: knowledge base for software delivery practices enabling fast and safe AI-assisted development";
  inputs.self.submodules = true;
  inputs.graft.url = "github:danielnaab/tuteur/v0.2.1";
  outputs = inputs: inputs.graft.lib.mkFlake { inherit inputs; };
}
