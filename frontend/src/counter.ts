let BACKEND_URL = import.meta.env.VITE_BACKEND_URL


export async function setupCounter(element: HTMLButtonElement) {
  let counter = 0
  let username = ""
  const setCounter = (count: number) => {
    counter = count
    element.innerHTML = `count is ${counter}`
    fetch(`${BACKEND_URL}/set_counter`, {
      method: "POST",
      body: JSON.stringify({
        username: username,
        value : count
      }),
      headers: {
        "Content-type": "application/json; charset=UTF-8"
      }
    })
  }
  document.getElementById("submit-username")!.addEventListener(
      "click",
      async () => {
          username = (document.getElementById("username") as HTMLInputElement).value;
          submit_username(username)
          setCounter(
              await fetch(`${BACKEND_URL}/get_counter`, {
                  method: "POST",
                  body: JSON.stringify({
                      username: username
                  }),
                  headers: {
                      "Content-type": "application/json; charset=UTF-8"
                  }
              })
                  .then((response) => response.json())
                  .then((data) => parseInt(data))
          )
      }
  )
  element.addEventListener('click', () => setCounter(counter + 1))
  setCounter(
      await fetch(`${BACKEND_URL}/get_counter`, {
        method: "POST",
        body: JSON.stringify({
          username: username
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
      })
          .then((response) => response.json())
          .then((data) => parseInt(data))
  )

    const submit_username = (value : string) => {
      document.getElementById("username-info")!
          .textContent = "Username is: "+value
    }
}
