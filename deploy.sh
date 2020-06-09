_env=$1
_clientId=$2
_clientSecret=$3
_password=$4
_userAgent=$5
_username=$6
_imagetag=bpb-$_env

echo $_env
echo $_username
echo $_password
echo $_userAgent
echo $_clientId
echo $_clientSecret

docker build \
--build-arg env=$_env \
--build-arg username=$_username \
--build-arg password=$_password \
--build-arg userAgent=$_userAgent \
--build-arg clientId=$_clientId \
--build-arg clientSecret=$_clientSecret \
--no-cache -t "$_imagetag" .

heroku container:push web

heroku container:release web