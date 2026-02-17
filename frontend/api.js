// ----------- UPDATE THIS WHEN DEPLOYED --------------
const API = "http://127.0.0.1:8000/api";

async function post(url,body,auth=true){
    return fetch(API+url,{
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            ...(auth && {"Authorization":"Bearer "+localStorage.getItem("token")})
        },
        body:JSON.stringify(body)
    }).then(r=>r.json());
}

async function get(url,auth=true){
    return fetch(API+url,{
        headers: auth ? {"Authorization":"Bearer "+localStorage.getItem("token")}:{}
    }).then(r=>r.json());
}
