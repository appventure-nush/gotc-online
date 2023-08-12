let BACKEND_URL = import.meta.env.VITE_BACKEND_URL


export function setupUserForm(element: HTMLDivElement) {
    let result = "waiting for input"
    let curr_user = ""
    // @ts-ignore
    let activity_pinger_id : NodeJS.Timer = 0
    element.innerHTML = `
<p style="border: white; border-width: 5px" id = "userform_status_top">Sign In:</p>
<input type="text" id = "username_textin" value="" placeholder="enter username">
<button type="submit" id = "userform_butt" >sign in</button> <br>
<button type="submit" id = "signout_butt" disabled="disabled">sign out</button>
<p style="border: white; border-width: 5px" id = "userform_status_bottom">${result}</p>
`
    element.children.namedItem("userform_butt")!.addEventListener(
        "click",
        () => {
            let proposed_name = String((element.children.namedItem("username_textin") as HTMLInputElement).value)
            if (proposed_name === ""){
                element.querySelector<HTMLParagraphElement>("#userform_status_bottom")!.innerHTML = "Please enter a username"
            }
            else submit(proposed_name)
        }
    )

    element.children.namedItem("signout_butt")!.addEventListener(
        "click",
        () => {
            signout_submit()
        }
    )



    const submit = (value : string) => {
        element.querySelector<HTMLParagraphElement>("#userform_status_bottom")!.innerHTML = "sending sign in request..."
        // send a post request to the calculate part of the backend
        // body of post request is a json
        // first 3 parts of json are just fluff, the actual thing that matters now is the value : value part
        fetch(`${BACKEND_URL}/sign_in`, {
            method: "POST",
            body: JSON.stringify({
                proposed_username : value,
                login_session_key : localStorage.getItem("LoginSessionKey")
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        })
            // this results in a response promise that promises some sort of response
            // will be received from where the post was sent to


            .then((response) => {
                if(!response.ok) return Promise.reject(response)
                else return response.text()
            })
            .then((json_text) => {
                let json_response = JSON.parse(json_text)
                if(json_response["login_success"] === true) {
                    curr_user = json_response["confirmed_username"]
                    localStorage.setItem("LoginSessionKey",json_response["login_session_key"])
                    refreshText(json_response)
                    activity_pinger_id = setInterval(activity_ping, 20_000)
                    element.querySelector<HTMLButtonElement>("#userform_butt")!.disabled = true
                    element.querySelector<HTMLButtonElement>("#signout_butt")!.disabled = false
                    //emit a sign in event with current user's username in detail param
                    //emitted on document for ease of listening
                    window.document.dispatchEvent(new CustomEvent("SignInEvent", {detail:curr_user}))
                }
                else {
                    refreshText(json_response)
                }
            })

            .catch(error => {
                refreshText(error)
            });
    }

    const signout_submit = () => {
        fetch(`${BACKEND_URL}/sign_out`, {
            method: "POST",
            body: JSON.stringify({
                username : curr_user
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        })
            // this results in a response promise that promises some sort of response
            // will be received from where the post was sent to


            .then((response) => {
                if(!response.ok) return Promise.reject(response)
                else return response.text()
            })
            .then((json_text) => {
                let json_response = JSON.parse(json_text)
                if(json_response["signout_success"] === true) {
                    signout(json_response["text"])
                }
            })

            .catch(error => {
                refreshText(error)
            });
    }

    const activity_ping = () => {
        if(curr_user !== "" && window.document.hasFocus()) {
            element.querySelector<HTMLParagraphElement>("#userform_status_bottom")!.innerHTML = "pinging for activity..."
            // send a post request to the calculate part of the backend
            // body of post request is a json
            // first 3 parts of json are just fluff, the actual thing that matters now is the value : value part
            fetch(`${BACKEND_URL}/user_activity_ping`, {
                method: "POST",
                body: JSON.stringify({
                    username: curr_user
                }),
                headers: {
                    "Content-type": "application/json; charset=UTF-8"
                }
            })
                // this results in a response promise that promises some sort of response
                // will be received from where the post was sent to


                .then((response) => {
                    if (!response.ok) return Promise.reject(response)
                    else return response.text()
                })
                .then((json_text) => {
                    let json_response = JSON.parse(json_text)
                    if (json_response["still_active"] === true) {
                        element.querySelector<HTMLParagraphElement>("#userform_status_bottom")!.innerHTML = json_response["text"]
                    } else {
                        signout(json_response["text"])
                    }
                })

                .catch(error => {
                    refreshText(error)
                });
        }
    }

    const check_if_still_signed_in = () => {
        if(curr_user !== "") {
            element.querySelector<HTMLParagraphElement>("#userform_status_bottom")!.innerHTML = "pinging for activity..."
            // send a post request to the calculate part of the backend
            // body of post request is a json
            // first 3 parts of json are just fluff, the actual thing that matters now is the value : value part
            fetch(`${BACKEND_URL}/activity_status_request`, {
                method: "POST",
                body: JSON.stringify({
                    username: curr_user
                }),
                headers: {
                    "Content-type": "application/json; charset=UTF-8"
                }
            })
                // this results in a response promise that promises some sort of response
                // will be received from where the post was sent to


                .then((response) => {
                    if (!response.ok) return Promise.reject(response)
                    else return response.text()
                })
                .then((json_text) => {
                    let json_response = JSON.parse(json_text)
                    if (json_response["still_active"] === true) {
                        element.querySelector<HTMLParagraphElement>("#userform_status_bottom")!.innerHTML = json_response["text"]
                    } else {
                        signout(json_response["text"])
                    }
                })

                .catch(error => {
                    refreshText(error)
                });
        }
    }

    window.document.onfocus = check_if_still_signed_in

    const refreshText = (json_response : any) => {
        // update result variable and result element
        // (vue can automatically update element when variable is updated im too lazy to find out how to use vue)
        // plain vite seems to work anyway so I ain't complaining
        if (json_response["login_success"]) element.querySelector<HTMLParagraphElement>("#userform_status_top")!.innerHTML = json_response["text"]
        element.querySelector<HTMLParagraphElement>("#userform_status_bottom")!.innerHTML = json_response["text"]
    }

    const signout = (json_response_text : string) => {
        clearInterval(activity_pinger_id)
        curr_user = ""
        element.querySelector<HTMLParagraphElement>("#userform_status_top")!.innerHTML = "Sign In:"
        element.querySelector<HTMLParagraphElement>("#userform_status_bottom")!.innerHTML = json_response_text
        element.querySelector<HTMLButtonElement>("#userform_butt")!.disabled = false
        element.querySelector<HTMLButtonElement>("#signout_butt")!.disabled = true
        //emit sign out event to notify listeners of a sign out
        //emitted on document for ease of listening
        window.document.dispatchEvent(new CustomEvent("SignOutEvent"))
    }



}

