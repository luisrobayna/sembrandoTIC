window.addEventListener('load',()=>{
    const API_REST = "http://127.0.0.1:5001/api/usuario/login"
    async function create_user(data) {
        let options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: "omit",
            body: JSON.stringify(data)
        }

        let res  = {
            "status":"",
            "body": ""
        }
        const response = await fetch(API_REST, options)
        let info = await response.json()
        if (response.status == 200){
            res = {
                "status": response.status,
                "body":info
            }
                return res
        }else{
            return info.message
        }
    }

    if (localStorage.getItem('token')){
        window.location.href = "/home"
    }else{
        let singIn = document.getElementById('sing-in-l')
        let signUp = document.getElementById('sing-up-r')
        let formContainer = document.getElementById('formContainer')
        let alert = document.getElementById('alert')
        let email = document.getElementById('email')
        let password = document.getElementById('password')
        singIn.addEventListener('click',()=>{
            window.location.href="login"
        })
        signUp.addEventListener('click',()=>{
            window.location.href ="registro"
        })



        formContainer.addEventListener('submit', async (e) => {
            e.preventDefault()
            info = {
                "email": email.value,
                "password": password.value
            }
            let response = await create_user(info)
            if (response.status == 200){
                    localStorage.setItem('token',response.body.response)
                    window.location.href = "/home"
            }else{
                alert.classList.add('alert')
                alert.innerHTML = response
            }
        })
    }
})