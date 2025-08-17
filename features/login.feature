Feature: Login en SauceDemo
  Como usuario
  Quiero iniciar sesión
  Para acceder al inventario

  @ui
  Scenario: Login exitoso
    Given que estoy en la página de login
    When inicio sesión con usuario "standard_user" y clave "secret_sauce"
    Then debería ver el inventario

  @ui
  Scenario: Login inválido muestra error
    Given que estoy en la página de login
    When inicio sesión con usuario "usuario_falso" y clave "clave_incorrecta"
    Then debería ver un mensaje de error que contiene "Username and password do not match"
