# El_Pinguino_que_Sabia_Demasiado_challenge_5
Diseñar un Servicio de Logging Distribuido, múltiples servicios simulados, envíen sus logs a un servidor central, guardando y analiza todo

***
1. Diseñar un servicio de loggin distribuido

Múltiples servicios simulados (aka script random tiren errores falsos) envíen sus logs a un servidor central, que guarde y analice
***
2 Obejtivo tecnico
- Construir un sistema de registros distribuidos
- Servicios simulados que generen logs y los envíen por http
- un servidor central de registros que recibe, válida y guarda y devuelve registros
- Autenticación con tokens para evitar registros anónimos
- Endpoint/logs para recibir y consultar registros, con filtros de fecha
- Guardado en base de datos,

***
3 crear Servicios simulados (logging)
 3.1 Simular servicios que:
- Generen registros falsos()
	- Envíen los registros en formato JSON a un servidor central con método Post
	- incluyendo el headertoken válido con el formato:
	Authorization: token ("tu_token_aqui")

		3.1.1 Cada log debe contener:
			- Timestamp: fecha y hora exacta del evento
			- service: nombre del servicio que lo genero
			- severity: nivel (Info, Debug, Error, etc.)
			- message: Descripción de lo que pasó (o no paso)
		

	3.2 Servicios centrales (backend )
- Recibir logs enviados a post/logs
- Verificar el token autenticacion
- Guarde registros en base de datos
- Soportar múltiples logs enviados a la vez 
- Crear un punto final para consultar registros: GET/Logs
***	
4 autenticacion
- crear lista manual de tokens válidos para servicios
- Cada servicio debe enviar su token en el autorizador
- Si no es válido, el servidor responde con error y un mensaje
***
5. Checklist de Entrega
	- Múltiples servicios simulados generando registros
	- Logs enviados en JSON con POST /logs
	- Logs guardados correctamente en base de datos
	- Punto final GET /logs con filtros funcionales
	- Tokens únicos por servicio y verificación en el servidor
	- Respuestas HTTP claras y funcionales
	- Código comentado 