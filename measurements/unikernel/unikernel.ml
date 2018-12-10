open String
open Lwt.Infix
open Printf
open Cohttp



module Main (C:Mirage_types_lwt.CONSOLE) (CON:Conduit_mirage.S) = struct



  module Server = Cohttp_mirage.Server(Conduit_mirage.Flow)

  let yaks_control_keyword = "yaks"
  let yaks_control_uri_prefix = "/"^yaks_control_keyword
  (**********************************)
  (*      helpers functions         *)
  (**********************************)

  let starts_with a b =
    let len1 = String.length b
    and len2 = String.length a in
    if len1 < len2 then false else
      let rec aux i =
        if i < 0 then false else
          let sub = String.sub b i len2 in
          if (sub = a) then true else aux (pred i)
      in
      aux (len1 - len2)

  let query_to_string query =
    List.map (fun (n,v) -> Printf.sprintf "%s=%s" n (String.concat "," v)) query
    |> String.concat "&"


  let set_cookie key value =
    let cookie = Cohttp.Cookie.Set_cookie_hdr.make (key, value) in
    Cohttp.Cookie.Set_cookie_hdr.serialize ~version:`HTTP_1_0 cookie

  let string_of_cookies header =
    Cookie.Cookie_hdr.extract header |>
    List.fold_left (fun acc (k, v) -> acc^" , "^k^"="^v) ""

  (**********************************)
  (*        Error replies           *)
  (**********************************)

  let string_of_stream stream =
    let s = List.map Cstruct.to_string stream in
    Lwt.return (String.concat "" s)

  let empty_path =
    Server.respond_string ~status:`OK ~body:(
      "{\"status\":\"ok\"")
      ()
  let execute_http_request _ req body =
    let meth = req |> Request.meth in
    let uri = req |> Request.uri in
    let path = uri |> Uri.path  in
    let query = uri |> Uri.query in
    let headers = req |> Request.headers in
    ignore @@  Logs.debug (fun m -> m "[FER] HTTP req: %s %s?%s with cookie: %s" 
                              (Code.string_of_method meth) path (query_to_string query)
                              (Cookie.Cookie_hdr.extract headers
                               |> List.find_opt (fun (key, _) -> starts_with "is.yaks" key)
                               |> function | Some(k,v) -> k^"="^v | _ -> ""));
    if path = "/" then
      empty_path
    else
      empty_path
  (* (match path with 
     | Some selector -> execute_data_operation meth selector headers body
     | None -> invalid_path path) *)


  let start console conduit =
    Logs.set_level ~all:true (Some Logs.Debug);
    (* let http_callback _conn req body = execute_http_request req body in *)
    let spec = Server.make ~callback:execute_http_request () in
    let tcp = `TCP 80 in 
    CON.listen conduit tcp (Server.listen spec)
end