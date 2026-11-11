{
  description = "delivery-practices: knowledge base for software delivery practices enabling fast and safe AI-assisted development";

  inputs = {
    graft.url = "github:danielnaab/graft/v2.9.0";

    # Each `flake = false` input is a scion, grafted into scions/<name>/ (https://github.com/danielnaab/graft).
    meta-knowledge-base = { url = "github:danielnaab/meta-knowledge-base/v1.1.0"; flake = false; };
    living-specifications = { url = "github:danielnaab/living-specifications/v1.0.2"; flake = false; };
    python-starter = { url = "github:danielnaab/python-starter/v1.3.0"; flake = false; };
  };

  outputs = inputs: inputs.graft.lib.mkFlake { inherit inputs; };
}
