let BACKEND_URL = import.meta.env.VITE_BACKEND_URL


export async function setupCounter(element: HTMLButtonElement) {
  let counter = 0
    // todo: disable counter when username is ""
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

  document.addEventListener("SignInEvent", async function (e: { detail: string; }) {
      username = e.detail

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
  })

    document.addEventListener("SignOutEvent", async function () {
        username = ""

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
    })

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
}
