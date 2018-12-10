open Mirage

let server =
  (* let network =
    (generic_stackv4 default_console tap0)
    (socket_stackv4 default_console [Ipaddr.V4.any])
  in *)
  conduit_direct (dhcp_ipv4_stack default_network)



  let handler =
    let packages = [package "cohttp-mirage";  package "lwt_ppx"; package "logs"; package "cmdliner"] in
  foreign ~packages
    "Unikernel.Main" (console @-> conduit @-> job)

let () =
register "http_service" [handler $ default_console $ server]