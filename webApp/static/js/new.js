window.addEventListener('load',async()=>{
    //Function to get the new
    async function get_new(id){
        let res  = {
            "status":"",
            "body": ""
        }
        let response = await fetch(API_NEW + id)
        if (response.status == 200){
            res.status = response.status
            res.body = await response.json()
            return res
        }else{
            return response.status
        }
    }

    //function delete new
    async function delete_new(token,id_new){
        let options = {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: "omit",
            body: JSON.stringify(token)
        }
        const response = await fetch(API_NEW + id_new, options)
        return response.status
    }

    //Function to update new
    async function update_new(data,id_new) {
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
        const response = await fetch(API_NEW+id_new, options)
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

    //Function to get user_name
    async function get_user(token){
        const response = await fetch(API_VERIFY,{method:'GET',
        headers: {'Authorization': 'Bearer '+token}})
        return response.json()
    }

    //Function to get all the comment in the new
    async function get_comment_new(id){
        let res  = {
            "status":"",
            "body": ""
        }

        let response = await fetch(API_NEW + id+"/comment")
        if (response.status == 200){
            res.status = response.status
            res.body = await response.json()
            return res
        }else{
            return response.status
        }
        
    }
    

    //Functio to create a comment in the new
    async function create_comment(data,id) {
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
        const response = await fetch(API_NEW + id+"/comment", options)
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

    //function delete comment
    async function delete_comment(token,id_new,id_comment){
        let options = {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: "omit",
            body: JSON.stringify(token)
        }
        const response = await fetch(DELETE_COMMENT+id_new+"/comment/"+id_comment, options)
        return response.status
    }

    //Function to update comment
    async function update_comment(data,id_new,id_comment) {
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
        const response = await fetch(DELETE_COMMENT+id_new+"/comment/"+id_comment, options)
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
    





    /*********************showing the news*************************/ 
    const API_VERIFY = "http://127.0.0.1:5001/api/verify/token"
    const API_NEW = "http://127.0.0.1:5001/api/noticia/"
    const DELETE_COMMENT ="http://127.0.0.1:5001/api/noticia/"
    const valores = window.location.href;
    let url_info = valores.split("/")
    let param = url_info[4]
    let content_new = document.getElementById('content_new')
    let content_comment = document.getElementById('comments')
    let options_new = document.getElementById('options_new')
    let info_new = await get_new(param)
    if (info_new.status == 200){
        content_new.innerHTML = `
        <h1 class="title_new">${info_new.body.article.title}</h1>
        <p class="date_new">${info_new.body.article.date}</p>
        <p class="description_new">${info_new.body.article.description}</p>
        <div id="image_new">
            <img id="image_content" src="/static/img/img_web/${info_new.body.article.image}">
        </div>
        `
    }else{
        window.location.href = "/noticias"
    }

    if (localStorage.getItem('token')){
        let user_name = await get_user(localStorage.getItem('token'))
        if (user_name.user_name == "adminMaster01" || user_name.user_name == "adminMaster02"){
            options_new.style = 'display:block'
        }
    }


    /*********************Delete the new*************************/ 

    let delete_new_button = document.getElementById('delete_new')
    delete_new_button.addEventListener('click', async()=>{
        let delete_new_response = await delete_new({'token':localStorage.getItem('token')},param)
        window.location.href = "/noticias"
    })

    /*********************Update the new*************************/ 

    let update_new_button = document.getElementById('edit_new')
    let content_new_update = document.getElementById('content_new')
    let title_new = document.getElementsByClassName('title_new')
    let description = document.getElementsByClassName('description_new')
    let image_content = document.getElementById('image_content')
    let title_content = title_new[0].textContent
    let image = image_content.getAttribute('src').split('/')[4]
    update_new_button.addEventListener('click',()=>{
        content_new.innerHTML = `
        <form action="" method="put" id="form_new_update">
            <label for="title">Titulo de la noticia</label><br>
            <input type="text" name="title" id="title_new"><br>
            <label for="description">Descripcion de la noticia</label><br>
            <textarea name="decription" id="description">${description[0].textContent}</textarea><br>
            <input type="submit" id="public_new" value="Publicar">
        </form>
        `
        options_new.style = 'display:none'
        let tile_new_input = document.getElementById('title_new')
        let text_area_update = document.getElementById('description')
        let form_new_update = document.getElementById('form_new_update')
        tile_new_input.value = title_content
        form_new_update.addEventListener('submit',async(e)=>{
            e.preventDefault()
            let respon_udate = await update_new({"title":tile_new_input.value,
                                                "description":text_area_update.value,
                                                "image":image,
                                                "token":localStorage.getItem('token')},param)
            
            window.location.href ="/noticia/"+param
            
            
        })

    })







    /*********************showing the comments*************************/ 
    let comment_id = []
    let comment_response = await get_comment_new(param)
    let contador = []
    let user_action = ""
    let id_comment_admin = []
    let form_comment = document.getElementById('form_comment')
    if (comment_response.status == 200){
        let comments = comment_response.body.response.commentNew
        comments = comments.sort(function(a, b){return b - a});

        for(let comment of comments){
            if (!localStorage.getItem('token')){
                form_comment.style.display = "none"

                content_comment.innerHTML+= `
                <div class="comment_user">
                    <div class="user_image">
                        <img src="/static/img/img_web/${comment.pictureProfile}" alt="">
                    </div>
                    <div class="comment_info">
                        <p class="user_name"><a href="/usuario/perfil/${comment.user}">${comment.user}</a></p>
                        <p class="public_date">${comment.date}</p>
                        <p class="public_description">${comment.description}</p>
                    </div>
                </div>
                `
                contador.push('vacio')
            }else{
                user_name = await get_user(localStorage.getItem('token')) 
                if(user_name.user_name == "adminMaster01" || user_name.user_name == "adminMaster02"){
                    if(user_name.user_name == comment.user){
                        user_action = user_name.user_name
                        comment_id.push(comment.idComment)
                        id_comment_admin.push(comment.idComment)
                        content_comment.innerHTML+=`
                        <div class="comment_user">
                            <div class="user_image">
                                <img src="/static/img/img_web/${comment.pictureProfile}" alt="">
                            </div>
                            <div class="comment_info">
                                <p class="user_name"><a href="#">${comment.user}</a></p>
                                <p class="public_date">${comment.date}</p>
                                <p class="public_description">${comment.description}</p>
                                <div class="options_comment">
                                    <span class="edit_comment">Editar</span>
                                    <span class="delete_comment">Borrar</span>
                                </div>
                            </div>
                            
                        </div>
                        `  
                     contador.push('lleno')
                    }else{
                        comment_id.push(comment.idComment)
                        content_comment.innerHTML+=`
                        <div class="comment_user">
                            <div class="user_image">
                                <img src="/static/img/img_web/${comment.pictureProfile}" alt="">
                            </div>
                            <div class="comment_info">
                                <p class="user_name"><a href="#">${comment.user}</a></p>
                                <p class="public_date">${comment.date}</p>
                                <p class="public_description">${comment.description}</p>
                                <div class="options_comment">
                                    <span class="delete_comment">Borrar</span>
                                </div>
                            </div>
                        </div>
                        `
                        contador.push('vacio')
                    }
                }else if(user_name.user_name == comment.user){
                    comment_id.push(comment.idComment)
                    content_comment.innerHTML+=`
                        <div class="comment_user">
                            <div class="user_image">
                                <img src="/static/img/img_web/${comment.pictureProfile}" alt="">
                            </div>
                            <div class="comment_info">
                                <p class="user_name"><a href="#">${comment.user}</a></p>
                                <p class="public_date">${comment.date}</p>
                                <p class="public_description">${comment.description}</p>
                                <div class="options_comment">
                                    <span class="edit_comment">Editar</span>
                                    <span class="delete_comment">Borrar</span>
                                </div>
                            </div>
                            
                        </div>
                        `  
                     contador.push('lleno')
                }else{
                    content_comment.innerHTML+= `
                    <div class="comment_user">
                        <div class="user_image">
                            <img src="/static/img/img_web/${comment.pictureProfile}" alt="">
                        </div>
                        <div class="comment_info">
                            <p class="user_name"><a href="#">${comment.user}</a></p>
                            <p class="public_date">${comment.date}</p>
                            <p class="public_description">${comment.description}</p>
                        </div>
                    </div>
                 `
                 contador.push('vacio')
                }
            }
        }   
    }else{
        content_comment.innerHTML = `
        <div class="comment_user">
            <div id="no_comments">
                <p>Se el primero en comentar</p>
            </div>
        </div>
        `
        if (!localStorage.getItem('token')){
            form_comment.style.display = "none"
        }

    }

    

    /*********************creating the comments*************************/ 
   
    let comment_description = document.getElementById('create_comment')
    form_comment.addEventListener('submit',async(e)=>{
        e.preventDefault()
        let comment_created = await create_comment({'description': comment_description.value,
                                            'token':localStorage.getItem('token')},param)
        window.location.href='/noticia/'+param
    })



    /*********************Delete comment*************************/ 

    let button_del_comment = document.getElementsByClassName('delete_comment')

    for(let i = 0; i< button_del_comment.length; i++){
        button_del_comment[i].addEventListener("click", async()=>{
            let delete_response = await delete_comment({"token":localStorage.getItem('token'),},param,comment_id[i])
            window.location.href ="/noticia/"+param
        })
    }

    /*********************Update comment*************************/ 
    let button_edit_comment = document.getElementsByClassName('edit_comment')
    let class_comment = document.getElementsByClassName('comment_user')
    let content_area = document.getElementsByClassName('public_description')
    let segundo_contador = 0
    let aux_class = []
    let aux_description = []
    for(let state of contador){
        if(state == "lleno"){
            aux_class.push(class_comment[segundo_contador])
            aux_description.push(content_area[segundo_contador].textContent)
        }
        segundo_contador++
    }

    for(let i = 0; i< button_edit_comment.length; i++){
        button_edit_comment[i].addEventListener("click", async()=>{
            aux_class[i].innerHTML=`
                <form action="" method="put" id="form_comment_update">
                    <textarea name="description" id="create_comment_update">${aux_description[i]}</textarea>
                    <input type="submit" name="sendComment" id="update_comment" value="Comentar">
                </form>
            `
            let form_comment_update = document.getElementById('form_comment_update')
            form_comment_update.addEventListener('submit',async(e)=>{
                e.preventDefault()
                
                let text_area = document.getElementById('create_comment_update')
                if(user_action.length > 0){
                    let upate_response = await update_comment({"token":localStorage.getItem('token'),
                                                        "description":text_area.value},param,id_comment_admin[i])

                }else{
                    let upate_response = await update_comment({"token":localStorage.getItem('token'),
                                                        "description":text_area.value},param,comment_id[i])

                }
                window.location.href ="/noticia/"+param
            })
            
        })
    }


 



})