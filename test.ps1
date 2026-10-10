 = '{"themes":["default"]}';  =  | ConvertFrom-Json; if (-not .themes.Contains('PizzaTheme')) { .themes += 'PizzaTheme' }; .themes
