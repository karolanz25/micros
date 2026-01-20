tmr.delay(1000000)
gpio.mode(4, gpio.OUTPUT)
function blink(t)
	tmr.delay(200000)
	for i = 1, t do
		gpio.write(4,gpio.HIGH)
		tmr.delay(200000)
		gpio.write(4,gpio.LOW)
		tmr.delay(200000)
	end
	gpio.write(4,gpio.HIGH)
end

function start()
	gpio.mode(9,gpio.INPUT)
	gpio.mode(10,gpio.INPUT)
	gpio.write(4,gpio.LOW)
	if gpio.read(9) == 0 then
		if gpio.read(10) == 0 then
			blink(0)
			tmr.delay(2000000)
			uart.setup(0, 115200,8,0,1,1)
			print("config ap-st")
			collectgarbage()
			dofile('apst.lua')
		else
			blink(1)
			uart.setup(0, 115200,8,0,1,1)
			print("tcpServer-start")
			collectgarbage()
			dofile('tcpServer.lua')
		end
	else
		if gpio.read(10) == 0 then
			blink(2)
			tmr.delay(200000)
			if gpio.read(10) == 0 then
				file.remove('run.lua')
				uart.setup(0,115200,8,0,1,1)
				collectgarbage()
			else
				gpio.write(4,gpio.LOW)
				uart.setup(0,115200,8,0,1,1)
				collectgarbage()
			end
		else
			blink(3)
			if file.exists('run.lua') then
				uart.setup(0,115200,8,0,1,1)
				print("run")
				collectgarbage()
				dofile('run.lua')
			else
				uart.setup(0,115200,8,0,1,1)
				print('TCPClient-start')
				collectgarbage()
			end
		end
	end
end

start()
