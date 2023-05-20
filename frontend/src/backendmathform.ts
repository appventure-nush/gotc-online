let BACKEND_URL = import.meta.env.VITE_BACKEND_URL


export function setupBackendMathForm(element: HTMLDivElement) {
    let result = "waiting for input"
    element.innerHTML = `
<input type="number" id = "cnum" value="0">
<button type="submit" id = "butt">backend math</button>
<p style="border: white; border-width: 5px" id = "calculation_result">${result}</p>
`
    element.children.namedItem("butt")!.addEventListener(
        "click",
        () => submit(Number((element.children.namedItem("cnum") as HTMLInputElement).value))
    )

    const submit = (value : number) => {
        setResult("waiting for result...")
        // send a post request to the calculate part of the backend
        // body of post request is a json
        // first 3 parts of json are just fluff, the actual thing that matters now is the value : value part
        fetch(`${BACKEND_URL}/calculate`, {
            method: "POST",
            body: JSON.stringify({
                userId: 1,
                title: "Fix my bugs",
                completed: false,
                value : value
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        })
            // this results in a response promise that promises some sort of response
            // will be received from where the post was sent to

            // this converts the response promise into a string promise apparently
            // (resulting string should be the html text send by the flask)
            .then((response) => {
                if(!response.ok) return Promise.reject(response)
                else return response.text()
            })

            // promised string response is sent to set result
            .then((text) => {
                setResult(text)
            })
            .catch(error => {
                setResult(error)
            });
    }

    const setResult = (value : string) => {
        // update result variable and result element
        // (vue can automatically update element when variable is updated im too lazy to find out how to use vue)
        // plain vite seems to work anyway so I ain't complaining
        result = value
        element.querySelector<HTMLParagraphElement>("#calculation_result")!.innerHTML = result
    }

}

