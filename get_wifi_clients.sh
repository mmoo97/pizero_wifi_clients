while [ True ]
do
       	curl --silent 192.168.1.254/cgi-bin/devices.ha | grep -A 8 ">IPv4 Address / Name<" > unformatted_output.txt
	echo "File written."
	sleep 10
done
