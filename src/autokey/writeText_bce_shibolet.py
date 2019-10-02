from mcs import getData
n1 = getData('emailMatriculaWeb')
n2 = getData('passwordMatriculaWeb')
data.close()
keyboard.send_keys(n1)
keyboard.send_key('<tab>')
keyboard.send_keys(n2)
keyboard.send_key('<enter>')
