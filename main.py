
doc = '''
#%RAML 1.0
title: Codenation API
version: v1
mediaType: application/json #Indicar que a API deverá trabalhar com json
protocols: [HTTP, HTTPS]

securitySchemes:
    JWT:
        description: Autenticação com Token JWT.
        type: x-jwt
        describedBy:
            headers:
                Authorization:
                    description: Enviar o JSON Web Token no request.
                    type: string
                    required: true
            responses:
                401:
                    body:
                        application/json: |
                            {"error": "Authorization Required"}
        settings:
            signatures : ['HMAC-SHA256']


types:
    Auth:
        type: object
        discriminator: token
        properties:
            token : string
    
    User:
        type: object
        discriminator: user_id
        properties:
          name:
              type: string
              maxLength: 50
          password:
              type: string
              maxLength: 50
          email:
              type: string
              maxLength: 254
              pattern: ^[a-z0-9.]+@[a-z0-9]+\.[a-z]+(\.[a-z]+)?$
          last_login:
              type: date-only
          user_id: integer
          group_id: integer
        example:
            name: UsuarioTeste
            password: '123456'
            email: usuario@email.com.br
            last_login: 2020-07-01
            group_id: 1
            user_id: 1

    Group:
        type: object
        discriminator: group_id
        properties:
          name:
              type: string
        example:
            group_id: 5
            name: GrupoTeste


    Agent:
        type: object
        discriminator: agent_id
        properties:
          name:
              type: string
              maxLength: 50
          status:
              type: boolean
          environment:
              type: string
              maxLength: 20
          version:
              type: string
              maxLength: 5
          address:
              type: string
              maxLength: 39
          user_id:
              type: integer
        example:
            agent_id: 1
            user_id: 2
            name: AgenteTeste
            status: true
            environment: Teste
            version: v1
            address: 11.11.11.11

    Event:
        type: object
        discriminator: event_id
        properties:
          level:
              type: string
              maxLength: 20
          payload:
              type: string
          shelve:
              type: boolean
          date:
              type: datetime-only
          agent_id:
              type: integer
        example:
            event_id: 3
            level: Teste
            payload: Teste
            shelve: true 
            date: 2020-07-01T10:10:10
            agent_id: 3
    

/auth/token:
    post:
        description: Criar um novo Token
        body:             #Parâmetro de entrada um Token
            application/json:
                properties:
                    name: string
                    password: string
        responses:
            201:
                body:
                    application/json: Auth[]
            400:
                body:
                    application/json: |
                        {"error": "Bad Request."}

 
/agents:
    get:      
        description: Lista os agentes
        securedBy: JWT
        responses:         
            200:               
                body:
                    application/json: Agent[]
    post:     
        description: Inclui um novo agente.
        securedBy: JWT
        body:             
            application/json:
                properties:
                example: |
                    {"user_id": 2,
                    "name": "AgenteTeste",
                    "status": true,
                    "environment": "Teste",
                    "version": "v1",
                    "address": "11.11.11.11"
                    }
        responses:
            201:
                body:
                    application/json: Agent[]
            401:
                body:
                    application/json: |
                        {"error": "Authorization Required"}
    /{id}:
        get:      
            description: Lista agentes
            securedBy: JWT
            responses:         
                200:               
                    body:
                        application/json: Agent[]
                401:
                    body:
                        application/json: |
                            {"error": "Authorization Required"}
                404:
                    body:
                        application/json: |
                            {"error": "Not Found"}
        put:    
            description: Altera um agent por ID
            securedBy: JWT
            responses:
                200:               
                    body:
                        application/json: Agent[]
                401:
                    body:
                        application/json: |
                            {"error": "Authorization Required"}
                404:
                    body:
                        application/json: |
                            {"error": "Not Found"}
        delete: 
            description: Exclui um agent por ID
            securedBy: JWT
            responses:
                200:               
                    body:
                        application/json: Agent[]
                401:           #Parâmetro de saída no caso de erro inesperado
                    body:
                        application/json: |
                            {"error": "Authorization Required"}
                404:           #Parâmetro de saída no caso de erro inesperado
                    body:
                        application/json: |
                            {"error": "Not Found"}

    /{id}/events:
        get:      
            description: Lista evento de agente
            securedBy: JWT
            responses:         
                200:               
                    body:
                        application/json: Event[]
                401:
                    body:
                        application/json: |
                            {"error": "Authorization Required"}
                404:
                    body:
                        application/json: |
                            {"error": "Not Found"}
        post:     
            description: Inclui um Evento dentro do ID AGent
            securedBy: JWT
            body:
                application/json: Event[]
            responses:
                201:
                    body:
                        application/json: |
                            {"message": "Created"}
                401:
                    body:
                        application/json: |
                            {"error": "Authorization Required"}
                404:
                    body:
                        application/json: |
                            {"error": "Not Found"}
        put:    
            description: Altera um Evento de um Agent
            securedBy: JWT
            body:
                application/json: Event[]
            responses:
                200:               
                    body:
                        application/json: Event[]
                401:
                    body:
                        application/json: |
                            {"error": "Authorization Required"}
                404:
                    body:
                        application/json: |
                            {"error": "Not Found"}
        delete: 
            description: Exclui um Evento de um Agent
            securedBy: JWT
            body:
                application/json: Event[]
            responses:
                200:               
                    body:
                        application/json: Event[] 
                401:
                    body:
                        application/json: |
                            {"error": "Authorization Required"}
                404:
                    body:
                        application/json: |
                            {"error": "Not Found"}
        /{id}:
            get:      
                description: Lista evento de ID
                securedBy: JWT
                responses:         
                    200:               
                        body:
                            application/json: Event[]
                    401:
                        body:
                            application/json: |
                                {"error": "Authorization Required"}
                    404:
                        body:
                            application/json: |
                                {"error": "Not Found"}
            post:     
                description: Cria um Evento dentro do ID 
                securedBy: JWT
                body:
                    application/json: Event[]
                responses:
                    201:
                        body:
                            application/json: |
                                {"message": "Created"}
                    401:
                        body:
                            application/json: |
                                {"error": "Authorization Required"}
                    404:
                        body:
                            application/json: |
                                {"error": "Not Found"}
            put:    
                description: Altera um Evento de um Agent
                securedBy: JWT
                body:
                    application/json: Event[]
                responses:
                    200:               
                        body:
                            application/json: Event[]
                    401:
                        body:
                            application/json: |
                                {"error": "Authorization Required"}
                    404:
                        body:
                            application/json: |
                                {"error": "Not Found"}
            delete:
                description: Exclui um Evento de um Agent
                securedBy: JWT
                body:
                    application/json: Event[]
                responses:
                    200:               
                        body:
                            application/json: Event[] 
                    401:
                        body:
                            application/json: |
                                {"error": "Authorization Required"}
                    404:
                        body:
                            application/json: |
                                {"error": "Not Found"}

/groups:
    get:
        description: Lista os grupos
        securedBy: JWT
        responses:         
            200:               
                body:
                    application/json: Group[]
            401:
                body:
                    application/json: |
                        {"error": "Authorization Required"}
            404:
                body:
                    application/json: |
                        {"error": "Not Found"}
    post:
        description: Cria um novo grupo
        securedBy: JWT
        body:             #Parâmetro de entrada um usuário
            type: Group
        responses:
            201:
                body:
                    application/json: Group[] 
            401:
                body:
                    application/json: |
                        {"error": "Authorization Required"}
            404:
                body:
                    application/json: |
                        {"error": "Not Found"}
    put:
        description: Altera um grupo
        securedBy: JWT
        body:
            type: Group
        responses:
            200:               
                body:
                    application/json: Group[]
            401:
                body:
                    application/json: |
                        {"error": "Authorization Required"}
            404:
                body:
                    application/json: |
                        {"error": "Not Found"}
    delete:
        description: Exclui um grupo
        securedBy: JWT
        responses:
            200:               
                body:
                    application/json: Group[]
            401:
                body:
                    application/json: |
                        {"error": "Authorization Required"}
            404:
                body:
                    application/json: |
                        {"error": "Not Found"}
    /{id}:
        get:
            description: Lista os grupo por ID
            securedBy: JWT
            responses:         
                200:               
                    body:
                        application/json: Event[]
                401:
                    body:
                        application/json: |
                            {"error": "Authorization Required"}
                404:
                    body:
                        application/json: |
                            {"error": "Not Found"}
        put:
            description: Altera um grupo por ID
            securedBy: JWT
            body:
                type: Group
            responses:
                200:               
                    body:
                        application/json: Group[]
                401:
                    body:
                        application/json: |
                            {"error": "Authorization Required"}
                404:
                    body:
                        application/json: |
                            {"error": "Not Found"}
        delete: 
            description: Exclui um grupo por ID
            securedBy: JWT
            responses:
                200:               
                    body:
                        application/json: Group[]
                401:
                    body:
                        application/json: |
                            {"error": "Authorization Required"}
                404:
                    body:
                        application/json: |
                            {"error": "Not Found"}

/users:
    get:
        description: Lista os usuários
        securedBy: JWT
        responses:         
            200:               
                body:
                    application/json: User[]
            401:
                body:
                    application/json: |
                        {"error": "Authorization Required"}
            404:
                body:
                    application/json: |
                        {"error": "Not Found"}
    post:
        description: Cria um novo usuário
        securedBy: JWT
        body:             #Parâmetro de entrada um usuário
            type: User
        responses:
            201:
                body:
                    application/json: User[] 
            401:
                body:
                    application/json: |
                        {"error": "Authorization Required"}
            404:
                body:
                    application/json: |
                        {"error": "Not Found"}
    /{id}:
        get:
            description: Lista os usuários por ID
            securedBy: JWT
            responses:         
                200:               
                    body:
                        application/json: User[]
                401:
                    body:
                        application/json: |
                            {"error": "Authorization Required"}
                404:
                    body:
                        application/json: |
                            {"error": "Not Found"}
        put:
            description: Altera um usuário por ID
            securedBy: JWT
            body:
                type: User
            responses:
                200:               
                    body:
                        application/json: User[]
                401:
                    body:
                        application/json: |
                            {"error": "Authorization Required"}
                404:
                    body:
                        application/json: |
                            {"error": "Not Found"}
        delete:
            description: Exclui um usuário por ID
            securedBy: JWT
            responses:
                200:               
                    body:
                        application/json: User[]
                401:
                    body:
                        application/json: |
                            {"error": "Authorization Required"}
                404:
                    body:
                        application/json: |
                            {"error": "Not Found"}


'''
 