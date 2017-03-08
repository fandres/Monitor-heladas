pin=2 -- Correspondiente al GPIO4
gpio.mode(pin,gpio.OUTPUT)
aux=0
function blink ()

    if aux==0 then
        gpio.write(pin,gpio.HIGH)
        aux=1
    else
        gpio.write(pin,gpio.LOW)
        aux=0
    end
end

tmr.alarm(0,1000,1,blink) -- timer 0 como intervalo 1s
