{
  description = "delivery-practices: knowledge base for software delivery practices enabling fast and safe AI-assisted development";

  inputs = {
    graft.url = "github:danielnaab/graft/v2.12.0";

    # Each `flake = false` input is a scion, grafted into scions/<name>/ (https://github.com/danielnaab/graft).
    knowledge-base-kit = { url = "github:danielnaab/knowledge-base-kit/v2.1.0"; flake = false; };
    living-specifications = { url = "github:danielnaab/living-specifications/v1.0.2"; flake = false; };
    # The python-kit commit this project was generated or last updated from (v2.2.0): the
    # python-kit-upgrade workflow moves it with each update (copier's update doesn't touch this file),
    # so the pattern docs in scions/ match the template the code came from.
    python-kit     = { url = "github:danielnaab/python-kit/934f9c265b50455e3aa76aad9d196d2a9d92ed98"; flake = false; };
  };

  outputs = inputs: inputs.graft.lib.mkFlake { inherit inputs; };
}
