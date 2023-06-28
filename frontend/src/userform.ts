let BACKEND_URL = import.meta.env.VITE_BACKEND_URL


export function setupUserForm(element: HTMLDivElement) {
    let result = "waiting for input"
    // @ts-ignore
    let curr_user = ""
    element.innerHTML = `
<p style="border: white; border-width: 5px" id = "userform_status_top">sign in:</p>
<input type="text" id = "username_textin" value="" placeholder="enter username">
<button type="submit" id = "userform_butt">sign in</button>
<p style="border: white; border-width: 5px" id = "userform_status_bottom">${result}</p>
`
    element.children.namedItem("userform_butt")!.addEventListener(
        "click",
        () => submit(String((element.children.namedItem("username_textin") as HTMLInputElement).value))
    )

    const submit = (value : string) => {
        element.querySelector<HTMLParagraphElement>("#userform_status_bottom")!.innerHTML = "sending sign in request..."
        // send a post request to the calculate part of the backend
        // body of post request is a json
        // first 3 parts of json are just fluff, the actual thing that matters now is the value : value part
        fetch(`${BACKEND_URL}/sign_in`, {
            method: "POST",
            body: JSON.stringify({
                proposed_username : value
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
                    refreshText(json_response)
                }
                else {
                    refreshText(json_response)
                }
            })

            .catch(error => {
                refreshText(error)
            });
    }

    const refreshText = (json_response : any) => {
        // update result variable and result element
        // (vue can automatically update element when variable is updated im too lazy to find out how to use vue)
        // plain vite seems to work anyway so I ain't complaining
        if (json_response["login_success"]) element.querySelector<HTMLParagraphElement>("#userform_status_top")!.innerHTML = json_response["text"]
        element.querySelector<HTMLParagraphElement>("#userform_status_bottom")!.innerHTML = json_response["text"]
    }



}

