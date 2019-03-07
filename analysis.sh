./make.sh

echo "yeast"
lsd d datasets/yeast.el --complete results/yeast.out 
echo "yeast part"
lsd p datasets/yeast.el --complete results/yeast_part.out 
echo "yeast sung"
lsd p datasets/yeast.el --complete results/yeast_sung.out --sung    
echo "yeast brankovic"
lsd p datasets/yeast.el --complete results/yeast_brank.out --brankovic 
echo "yeast sung brankovic"
lsd p datasets/yeast.el --complete results/yeast_sung_brank.out --sung --brankovic 
echo "yeast onodera"
lsd o datasets/yeast.el --complete results/yeast_onodera.out 

echo "google"
lsd d datasets/web-Google.txt --complete results/google.out 
echo "google part"
lsd p datasets/web-Google.txt --complete results/google_part.out 
echo "google sung"
lsd p datasets/web-Google.txt --complete results/google_sung.out --sung    
echo "google brankovic"
lsd p datasets/web-Google.txt --complete results/google_brank.out --brankovic 
echo "google sung brankovic"
lsd p datasets/web-Google.txt --complete results/google_sung_brank.out --sung --brankovic 
echo "google onodera"
lsd o datasets/web-Google.txt --complete results/google_onodera.out 

echo "amazon"
lsd d datasets/Amazon0601.txt --complete results/amazon.out 
echo "amazon part"
lsd p datasets/Amazon0601.txt --complete results/amazon_part.out 
echo "amazon sung"
lsd p datasets/Amazon0601.txt --complete results/amazon_sung.out --sung     
echo "amazon brankovic"
lsd p datasets/Amazon0601.txt --complete results/amazon_brank.out --brankovic 
echo "amazon sung brankovic"
lsd p datasets/Amazon0601.txt --complete results/amazon_sung_brank.out --sung --brankovic 
echo "amazon onodera"
lsd o datasets/Amazon0601.txt --complete results/amazon_onodera.out 

echo "slashdot"
lsd d datasets/Slashdot0902.txt --complete results/slashdot.out 
echo "slashdot part"
lsd p datasets/Slashdot0902.txt --complete results/slashdot_part.out 
echo "slashdot sung"
lsd p datasets/Slashdot0902.txt --complete results/slashdot_sung.out --sung    
echo "slashdot brankovic"
lsd p datasets/Slashdot0902.txt --complete results/slashdot_brank.out --brankovic 
echo "slashdot sung brankovic"
lsd p datasets/Slashdot0902.txt --complete results/slashdot_sung_brank.out --sung --brankovic 
echo "slashdot onodera"
lsd o datasets/Slashdot0902.txt --complete results/slashdot_onodera.out 

echo "wikipedia"
lsd d datasets/WikiTalk.txt --complete results/wikipedia.out 
echo "wikipedia part"
lsd p datasets/WikiTalk.txt --complete results/wikipedia_part.out 
echo "wikipedia sung"
lsd p datasets/WikiTalk.txt --complete results/wikipedia_sung.out --sung 
echo "wikipedia brankovic"
lsd p datasets/WikiTalk.txt --complete results/wikipedia_brank.out --brankovic 
echo "wikipedia sung brankovic"
lsd p datasets/WikiTalk.txt --complete results/wikipedia_sung_brank.out --sung --brankovic 
echo "wikipedia onodera"
lsd o datasets/WikiTalk.txt --complete results/wikipedia_onodera.out 

echo "email"
lsd d datasets/Email-EuAll.txt --complete results/eumail.out 
echo "email part"
lsd p datasets/Email-EuAll.txt --complete results/eumail_part.out 
echo "email sung"
lsd p datasets/Email-EuAll.txt --complete results/eumail_sung.out --sung 
echo "email brankovic"
lsd p datasets/Email-EuAll.txt --complete results/eumail_brank.out --brankovic 
echo "email sung brankovic"
lsd p datasets/Email-EuAll.txt --complete results/eumail_sung_brank.out --sung --brankovic 
echo "email onodera"
lsd o datasets/Email-EuAll.txt --complete results/eumail_onodera.out 

echo "caida"
lsd d datasets/caida20071105_small.txt --complete results/caida.out 
echo "caida part"
lsd p datasets/caida20071105_small.txt --complete results/caida_part.out 
echo "caida sung"
lsd p datasets/caida20071105_small.txt --complete results/caida_sung.out --sung 
echo "caida brankovic"
lsd p datasets/caida20071105_small.txt --complete results/caida_brank.out --brankovic 
echo "caida sung brankovic"
lsd p datasets/caida20071105_small.txt --complete results/caida_sung_brank.out --sung --brankovic 
echo "caida onodera"
lsd o datasets/caida20071105_small.txt --complete results/caida_onodera.out 

echo "Gether results"
rm result.txt
for i in $( ls results/); do
     echo $i >> result.txt
     grep Elapsed results/$i|awk '{printf "%d\n", $5}'>> result.txt
done

