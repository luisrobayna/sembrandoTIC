window.addEventListener('load', async () => {
    //Function to get the post
    async function get_post(id) {
        let res = {
            "status": "",
            "body": ""
        }
        let response = await fetch(API_POST + id)
        if (response.status == 200) {
            res.status = response.status
            res.body = await response.json()
            return res
        } else {
            return response.status
        }
    }

    //Function to get user_name 
    async function get_user(token) {
        const response = await fetch(API_VERIFY, {
            method: 'GET',
            headers: { 'Authorization': 'Bearer ' + token }
        })
        return response.json()
    }


    //function delete post
    async function delete_post(token, id_post) {
        let options = {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: "omit",
            body: JSON.stringify(token)
        }
        const response = await fetch(API_POST + id_post, options)
        return response.status
    }


    //Function to update post
    async function update_post(data,id_post) {
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
        const response = await fetch(API_POST + id_post, options)
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


    //Function to get all the comment in the post
    async function get_comments_post(id){
        let res  = {
            "status":"",
            "body": ""
        }

        let response = await fetch(API_POST + id+"/comment")
        if (response.status == 200){
            res.status = response.status
            res.body = await response.json()
            return res
        }else{
            return response.status
        }
        
    }
    

    //Functio to create a comment in the post
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
        const response = await fetch(API_POST + id +"/comment", options)
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
    async function delete_comment(token,id_post,id_comment){
        let options = {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: "omit",
            body: JSON.stringify(token)
        }
        const response = await fetch(API_POST + id_post +"/comment/" + id_comment, options)
        return response.status
    }


     //Functio to update comment
     async function update_comment(data,id_post,id_comment) {
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
        const response = await fetch(API_POST + id_post + "/comment/"+id_comment, options)
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



    /*********************showing the post*************************/
    const API_VERIFY = "http://127.0.0.1:5001/api/verify/token"
    const API_POST = "http://127.0.0.1:5001/api/foro/post/"
    const DELETE_COMMENT = "http://127.0.0.1:5001/api/foro/post/"
    const valores = window.location.href;

    let url_info = valores.split("/")
    let param = url_info[5]
    let content_post = document.getElementById('content_post')
    let content_comment = document.getElementById('comments')
    let options_new = document.getElementById('options_new')
    let info_post = await get_post(param)
    if (info_post.status == 200) {
        content_post.innerHTML = `
        <h1 class="title_post" id="title_post">${info_post.body.response.post.title}</h1>
        <p class="user_name" id="user_post"><a href="/usuario/perfil/${info_post.body.response.post.userCreator}">${info_post.body.response.post.userCreator}</a></p>
        <p class="date_post" id="date_post">${info_post.body.response.post.date}</p>
        <p class="description_post" id="description_post">${info_post.body.response.post.description}</p>
        `
    } else {
        window.location.href = "/foro"
    }

    if (localStorage.getItem('token')) {
        let user_name = await get_user(localStorage.getItem('token'))
        if (user_name.user_name == info_post.body.response.post.userCreator){
            options_new.style = 'display:block'
        }else if(user_name.user_name == "adminMaster01" || user_name.user_name == "adminMaster02"){
            options_new.style = 'display:block'
            options_new.innerHTML = `
                <button id="delete_new">Eliminar</button>
            `
        }
    }


    /*********************Delete the post*************************/

    let delete_new_button = document.getElementById('delete_new')
    delete_new_button.addEventListener('click', async () => {
        let delete_post_response = await delete_post({ 'token': localStorage.getItem('token') }, param)
        window.location.href = "/foro"
    })




    /*********************Update the post*************************/ 

    let update_post_button = document.getElementById('edit_new')

    let title_post = document.getElementsByClassName('title_post')
    let description = document.getElementsByClassName('description_post')
    let title_content = title_post[0].textContent
    let user_name = await get_user(localStorage.getItem('token'))
    if (user_name.user_name == info_post.body.response.post.userCreator){
        update_post_button.addEventListener('click',()=>{
            content_post.innerHTML = `
            <form action="" method="put" id="form_post_update">
                <label for="title">Titulo del post</label><br>
                <input type="text" name="title" id="title_post_input"><br>
                <label for="description">Descripcion de la noticia</label><br>
                <textarea name="decription" id="description">${description[0].textContent}</textarea><br>
                <input type="submit" id="public_post" value="Publicar">
            </form>
            `
            options_new.style = 'display:none'
            let tile_post_input = document.getElementById('title_post_input')
            let text_area_update = document.getElementById('description')
            let form_post_update = document.getElementById('form_post_update')
            tile_post_input.value = title_content
            form_post_update.addEventListener('submit',async(e)=>{
                e.preventDefault()
                let respon_udate = await update_post({"title":tile_post_input.value,
                                                    "description":text_area_update.value,
                                                    "token":localStorage.getItem('token')},param)
                
                window.location.href ="/foro/post/"+param
                
                
            })
    
        })
        
    }

  



    /*********************showing the comments*************************/ 
    let comment_id = []
    let comment_response = await get_comments_post(param)
    let contador = []
    let user_action = ""
    let id_comment_admin = []
    let form_comment = document.getElementById('form_comment')
    if (comment_response.status == 200){

        let comments = comment_response.body.response.postComments
        comments = comments.sort(function(a, b){return b - a});

        for(let comment of comments){
            if (!localStorage.getItem('token')){
                content_comment.innerHTML+= `
                <div class="comment_user">
                    <div class="user_image">
                        <img src="/static/img/img_web/${comment.pictureProfile}" alt="">
                    </div>
                    <div class="comment_info">
                        <p class="user_name"><a href="/usuario/perfil/${comment.user_name}">${comment.user_name}</a></p>
                        <p class="public_date">${comment.date}</p>
                        <p class="public_description">${comment.description}</p>
                    </div>
                </div>
                `
                form_comment.style.display = "none"
                contador.push('vacio')
            }else{
                user_name = await get_user(localStorage.getItem('token')) 
                if(user_name.user_name == "adminMaster01" || user_name.user_name == "adminMaster02"){
                    if(user_name.user_name == comment.user_name){
                        user_action = user_name.user_name
                        comment_id.push(comment.idComment)
                        id_comment_admin.push(comment.idComment)
                        content_comment.innerHTML+=`
                        <div class="comment_user">
                            <div class="user_image">
                                <img src="/static/img/img_web/${comment.pictureProfile}" alt="">
                            </div>
                            <div class="comment_info">
                                <p class="user_name"><a href="/usuario/perfil/${comment.user_name}">${comment.user_name}</a></p>
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
                                <p class="user_name"><a href="/usuario/perfil/${comment.user_name}">${comment.user_name}</a></p>
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
                }else if(user_name.user_name == comment.user_name){
                    comment_id.push(comment.idComment)
                    content_comment.innerHTML+=`
                        <div class="comment_user">
                            <div class="user_image">
                                <img src="/static/img/img_web/${comment.pictureProfile}" alt="">
                            </div>
                            <div class="comment_info">
                                <p class="user_name"><a href="/usuario/perfil/${comment.user_name}">${comment.user_name}</a></p>
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
                            <p class="user_name"><a href="/usuario/perfil/${comment.user_name}">${comment.user_name}</a></p>
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
        window.location.href='/foro/post/'+param
    })


     /*********************Delete comment*************************/ 

     let button_del_comment = document.getElementsByClassName('delete_comment')

     for(let i = 0; i< button_del_comment.length; i++){
         button_del_comment[i].addEventListener("click", async()=>{
             let delete_response = await delete_comment({"token":localStorage.getItem('token'),},param,comment_id[i])
             window.location.href ="/foro/post/"+param
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
                window.location.href ="/foro/post/"+param
            })
            
        })
    }
    
})