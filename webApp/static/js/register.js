window.addEventListener('load', () => {
    const API_REST = "http://127.0.0.1:5001/api/usuario/registro"
    async function create_user(data) {
        let options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: "omit",
            body: JSON.stringify(data)
        }
        const response = await fetch(API_REST, options)
        let info = await response.json()
        if (response.status == 200){
                return response.status
        }else{
            return info.response
        }
    }

    if (localStorage.getItem('token')){
        window.location.href = "/home"
    }else{
        let singIn = document.getElementById('sing-in')
        let signUp = document.getElementById('sing-up')
        let formContainer = document.getElementById('formContainer')
        let user_name = document.getElementById('user_name')
        let email = document.getElementById('email')
        let password = document.getElementById('password')
        let alert = document.getElementById('alert')
        singIn.addEventListener('click', () => {
            window.location.href = "login"
        })
        signUp.addEventListener('click', () => {
            window.location.href = "registro"
        })

        formContainer.addEventListener('submit', async (e) => {
            e.preventDefault()
            info = {
                "user_name": user_name.value,
                "email": email.value,
                "password": password.value
            }
            if (info.user_name.length == 0) {
                alert.classList.add('alert')
                alert.innerHTML = "Ingrese nombre de usuario"
            } else if (info.email.length == 0) {
                alert.classList.add('alert')
                alert.innerHTML = "Ingrese correo"
            }else if (info.email.includes('@') == false  ||info.email.includes('.') == false ){
                alert.classList.add('alert')
                alert.innerHTML = "Ingrese un correo valido"
            }else if (info.password.length == 0) {
                alert.classList.add('alert')
                alert.innerHTML = "Ingrese contraseña"
            } else if(info.password.length < 6){
                alert.classList.add('alert')
                alert.innerHTML = "Ingrese contraseña con mas de 5 caracteres"
            }
            else{
                let response = await create_user(info)
                if (response == 200){
                    window.location.href = "login"
                }else{
                    alert.classList.add('alert')
                    alert.innerHTML = response
                }
            }

        })
    }

})