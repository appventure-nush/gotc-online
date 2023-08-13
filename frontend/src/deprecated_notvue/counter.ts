/*
THIS CODE IS NOW DEPRECATED
Since this project is going to use the Vue 3 framework from now on, this code has been converted to its vue equivilant
and is now deprecated.
 */

let BACKEND_URL = import.meta.env.VITE_BACKEND_URL


export async function setupCounter(element: HTMLButtonElement) {
  let counter = 0
  let username = ""
  // username cannot be ""
  element.disabled = true
  element.innerHTML = "sign in first"

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
      element.disabled = false

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

    document.addEventListener("SignOutEvent", function () {
        username = ""
        element.disabled = true
        element.innerHTML = "sign in first"
    })

  element.addEventListener('click', () => setCounter(counter + 1))
}
