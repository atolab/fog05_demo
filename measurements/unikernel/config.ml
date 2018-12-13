open Mirage


let config = {
  network = (Ipaddr.V4.Prefix.of_string_exn "192.168.122.0/24", Ipaddr.V4.of_string_exn "192.168.122.100")
}

let server =
  (* let network =
     (generic_stackv4 default_console tap0)
     (socket_stackv4 default_console [Ipaddr.V4.any])
     in *)
  conduit_direct (static_ipv4_stack ~config default_network)



let handler =
  let packages = [package "cohttp-mirage";  package "lwt_ppx"; package "logs"; package "cmdliner"] in
  foreign ~packages
    "Unikernel.Main" (console @-> conduit @-> job)

let () =
  register "http_service" [handler $ default_console $ server]