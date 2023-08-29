
# EJERCICIOS

1 - Cuándo y por qué se produce el error BrokenPipeError: [Errno 32] Broken pipe ?

- El problema es que la conexion se cierra antes de tiempo por lo que el cliente no puede enviar los datos al servidor. El mensaje de error seria que el cliente quiere escribir en un pipe que no lo accepta.
