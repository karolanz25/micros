-- init.lua
print("Esperando 5 segundos antes de iniciar...")

-- Creamos un temporizador
tmr.create():alarm(5000, tmr.ALARM_SINGLE, function()
    print("Iniciando conexión Wi-Fi...")
    
    -- Configuración de red
    wifi.setmode(wifi.STATION)
    wifi.sta.config({ssid="Claro_0699E3", pwd="T4R9W8X2J9F8"})
    
    wifi.eventmon.register(wifi.eventmon.STA_GOT_IP, function(T)
        print("\n¡Conectado! IP: "..T.IP)
        -- Aquí llamas a tu script principal
        -- dofile("mi_proyecto.lua")
    end)
end)
