{
  description = "delivery-practices: knowledge base for software delivery practices enabling fast and safe AI-assisted development";

  inputs = {
    graft.url = "github:danielnaab/graft/v2.9.0";

    # Each `flake = false` input is a scion, grafted into scions/<name>/ (https://github.com/danielnaab/graft).
    knowledge-base-kit = { url = "github:danielnaab/knowledge-base-kit/v2.0.0"; flake = false; };
    living-specifications = { url = "github:danielnaab/living-specifications/v1.0.2"; flake = false; };
    python-kit     = { url = "github:danielnaab/python-kit/v2.0.1"; flake = false; };
  };

  outputs = inputs: inputs.graft.lib.mkFlake { inherit inputs; };
}
