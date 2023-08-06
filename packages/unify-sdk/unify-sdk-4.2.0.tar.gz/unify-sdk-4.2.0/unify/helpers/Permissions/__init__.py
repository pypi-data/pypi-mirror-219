class Verbs:
    modifyworkspace = "modifyworkspace"
    list = "list"
    read = "read"
    write = "write"
    anyverb = "anyverb"
    everyverb = "everyverb"


class Domains:
    template = "template"
    pipeline = "pipeline"
    dataset = "dataset"
    graph = "graph"
    connector = "connector"
    permission = "permission"
    org_api = "org_api"
    workspace = "workspace"


class Effects:
    allow = "allow"
    deny = "deny"


class DisplayNames:
    everyone = "everyone"
    nobody = "nobody"
    everything = "everything"
    nothing = "nothing"


class SelectorBool:
    everyone = 1
    nobody = 2
    everything = 3
    nothing = 4


class SelectorType:
    user = "user"
    resource = "resource"


class ArtifactType:
    connector = "connector"
    dataset = "dataset"
    pipeline = "pipeline"
    graph = "graph"
    template = "template"
