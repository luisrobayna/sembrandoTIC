window.addEventListener('load',async()=>{
    async function get_profile(user){
        let res  = {
            "status":"",
            "body": ""
        }
        let response = await fetch(API_PROFILE + user)
        if (response.status == 200){
            let info = await response.json()
            res = {
                "status": response.status,
                "body":info
            }
                return res

        }else{
            return response.status
        }
    }


      //Function to get user_name
    async function get_user(token){
        const response = await fetch(API_VERIFY,{method:'GET',
        headers: {'Authorization': 'Bearer '+token}})
        return response.json()
    }


     //Function to update profile
     async function update_profile(data,user) {
        let options = {
            method: 'PUT',
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
        const response = await fetch(API_PROFILE+ user, options)
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

    //function delete account
    async function delete_account(token,user){
        let options = {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: "omit",
            body: JSON.stringify(token)
        }
        const response = await fetch(API_PROFILE + user, options)
        return response.status
    }



    const API_PROFILE = "http://127.0.0.1:5001/api/usuario/perfil/"
    const API_VERIFY = "http://127.0.0.1:5001/api/verify/token"
    const url = window.location.href;
    let url_info = url.split("/")
    let url_user = url_info[5]
    let profile = document.getElementById('profile')
    let options_profile = document.getElementById('options_profile')
    
    /****************************Get profile ********************************/
    let response_profile = await get_profile(url_user)

    if (response_profile.status == 200){
        let user_profile = response_profile.body.response[0]
        profile.innerHTML = `
        <h1>Prefil de usuario</h1>
        <div id="photo_profile">
            <img src="/static/img/img_web/${user_profile.profile_image}" alt="">
        </div>
        <div id="detail_profile">
            <p>Nombre completo: <span id="complete_name">${user_profile.full_name}</span></p>
            <p>Edad:<span id="age">${user_profile.age}</span></p>
            <p>Nombre de usuario:<span id="nick">${user_profile.user_name}</span></p>
            <p>Descripcion: <span id="desc_profile">${user_profile.description}</span></p>
        </div>
        `
        if (localStorage.getItem('token')){
            let user_name = await get_user(localStorage.getItem('token'))
            if (url_user == user_name.user_name){
                profile.innerHTML = `
                    <h1>Prefil de usuario</h1>
                    <div id="photo_profile">
                        <img src="/static/img/img_web/${user_profile.profile_image}" alt="">
                    </div>
                    <div id="detail_profile">
                        <p>Nombre completo: <span id="complete_name">${user_profile.full_name}</span></p>
                        <p>Edad:<span id="age">${user_profile.age}</span></p>
                        <p>Nombre de usuario:<span id="nick">${user_profile.user_name}</span></p>
                        <p>Descripcion: <span id="desc_profile">${user_profile.description}</span></p>
                    </div>
                    `
                    options_profile.style.display = "block"
            }else if(user_name.user_name == "adminMaster01" || user_name.user_name == "adminMaster02"){
                profile.innerHTML = `
                    <h1>Prefil de usuario</h1>
                    <div id="photo_profile">
                        <img src="/static/img/img_web/${user_profile.profile_image}" alt="">
                    </div>
                    <div id="detail_profile">
                        <p>Nombre completo: <span id="complete_name">${user_profile.full_name}</span></p>
                        <p>Edad:<span id="age">${user_profile.age}</span></p>
                        <p>Nombre de usuario:<span id="nick">${user_profile.user_name}</span></p>
                        <p>Descripcion: <span id="desc_profile">${user_profile.description}</span></p>
                    </div>
                    `
                    options_profile.style.display = "block"
                    options_profile.innerHTML = `
                    <button id="eliminate_account">Banear cuenta</button>
                    `
                }
            
        }else{
            profile.innerHTML = `
                    <h1>Prefil de usuario</h1>
                    <div id="photo_profile">
                        <img src="/static/img/img_web/${user_profile.profile_image}" alt="">
                    </div>
                    <div id="detail_profile">
                        <p>Nombre completo: <span id="complete_name">${user_profile.full_name}</span></p>
                        <p>Edad:<span id="age">${user_profile.age}</span></p>
                        <p>Nombre de usuario:<span id="nick">${user_profile.user_name}</span></p>
                        <p>Descripcion: <span id="desc_profile">${user_profile.description}</span></p>
                    </div>
                    `
        }
    }else{
        window.location.href = "/home"
    }

/*****************Profile update************************************* */
    if (localStorage.getItem('token')){
        let userName = await get_user(localStorage.getItem('token'))
            if (url_user == userName.user_name){
                let edit_profile = document.getElementById('edit_profile')
                let textArea = document.getElementById('desc_profile')
                let age_input = document.getElementById('age')
                let complete_name = document.getElementById('complete_name')
                console.log(textArea)
                let contentArea = textArea.textContent
                let contentFullName = complete_name.textContent
                let contentAge = age_input.textContent
                edit_profile.addEventListener('click',async()=>{

                    profile.innerHTML = `
                    <div id="edit">
                        <form action="/actualizar/perfil" method="post" id="form_edit" enctype="multipart/form-data">
                            <label for="full_name">Nombre Completo:</label><br>
                            <input type="text" name="full_name" id="input_full_name" value="${contentFullName}"><br>
                            <label for="age">Edad:</label><br>
                            <input type="text" name="age" id="input_age" value="${contentAge}"><br>
                            <label for="description">Descripcion</label><br>
                            <textarea name="description" id="area_description">${contentArea}</textarea><br>
                            <input type="text" name="user_name" value="${url_user}" style="display:none">
                            <input type="submit" id="edit_send" value="Publicar">
                            <div id="upload_img_input">
                                <input id="charge_image" type="file" name="file">
                                subir imagen...
                            </div>
                        </form>
                    </div>
                    `
                    
                    options_profile.style.display = "none"
                    
                })
            }
    }

    /******************Eliminate the user*********************/
    let eliminate_account = document.getElementById('eliminate_account')
    eliminate_account.addEventListener('click',async()=>{
        let user_action = await get_user(localStorage.getItem('token'))
        if (user_action.user_name == "adminMaster01" || user_action == "adminMaster02"){
            let ban_account = confirm('Estas seguro que queres banear esta cuenta?')
            if (ban_account == true){
                let response_ban = await delete_account({"token":localStorage.getItem('token')},url_user)
                window.location.href ="/home"
            }
        }else{
            let confirmssg = confirm('Estas seguro que quieres eliminar la cuenta?')
            console.log(confirmssg)
            if (confirmssg == true){
            let response_delete = await delete_account({"token":localStorage.getItem('token')},url_user)
            localStorage.removeItem('token')
            window.location.href = "/home"
            }
        }
       
    })

})

