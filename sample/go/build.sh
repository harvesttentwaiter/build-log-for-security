strace -e trace=execve,openat -f -o go.strace go install github.com/harvesttentwaiter/build-log-for-security/sample/go
python sha2build.py go.strace > go.sha2
# send go.sha2 
touch netrc
chmod 700 netrc
env | grep SENDBUILDLOG > netrc
sed -e 's/SENDBUILDLOG=/machine example.com login binkyUser password /' -i netrc
curl --netrc-file=netrc -F 'f=@go.sha2' -F 'prj=sample' example.com/target
