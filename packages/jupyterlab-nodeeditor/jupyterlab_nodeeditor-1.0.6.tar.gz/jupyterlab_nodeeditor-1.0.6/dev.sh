cd test_ext
jupyter lab > /dev/null 2>&1 & 
cd ..
jlpm run watch &
cd flume
yarn run start
