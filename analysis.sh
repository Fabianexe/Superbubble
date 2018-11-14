./make.sh

echo "yeast"
lsd datasets/yeast.el -r complete -o results/yeast.out
echo "yeast sung"
lsd datasets/yeast.el -r complete -o results/yeast_sung.out --sung       
echo "yeast brankovic"
lsd datasets/yeast.el -r complete -o results/yeast_brank.out --brankovic
echo "yeast sung brankovic"
lsd datasets/yeast.el -r complete -o results/yeast_sung_brank.out --sung --brankovic

echo "google"
lsd datasets/web-Google.txt -r complete -o results/google.out
echo "google sung"
lsd datasets/web-Google.txt -r complete -o results/google_sung.out --sung
echo "google brankovic"
lsd datasets/web-Google.txt -r complete -o results/google_brank.out --brankovic
echo "google sung brankovic"               
lsd datasets/web-Google.txt -r complete -o results/google_sung_brank.out --sung --brankovic

echo "amazon"
lsd datasets/Amazon0601.txt -r complete -o results/amazon.out
echo "amazon sung"
lsd datasets/Amazon0601.txt -r complete -o results/amazon_sung.out --sung 
echo "amazon brankovic"
lsd datasets/Amazon0601.txt -r complete -o results/amazon_brank.out --brankovic
echo "amazon sung brankovic"                 
lsd datasets/Amazon0601.txt -r complete -o results/amazon_sung_brank.out --sung --brankovic

echo "slashdot"
lsd datasets/Slashdot0902.txt -r complete -o results/slashdot.out
echo "slashdot sung"
lsd datasets/Slashdot0902.txt -r complete -o results/slashdot_sung.out --sung 
echo "slashdot brankovic"
lsd datasets/Slashdot0902.txt -r complete -o results/slashdot_brank.out --brankovic
echo "slashdot sung brankovic"                 
lsd datasets/Slashdot0902.txt -r complete -o results/slashdot_sung_brank.out --sung --brankovic

echo "wikipedia"
lsd datasets/WikiTalk.txt -r complete -o results/wikipedia.out
echo "wikipedia sung"
lsd datasets/WikiTalk.txt -r complete -o results/wikipedia_sung.out --sung 
echo "wikipedia brankovic"
lsd datasets/WikiTalk.txt -r complete -o results/wikipedia_brank.out --brankovic
echo "wikipedia sung brankovic"                 
lsd datasets/WikiTalk.txt -r complete -o results/wikipedia_sung_brank.out --sung --brankovic

echo "email"
lsd datasets/Email-EuAll.txt -r complete -o results/eumail.out
echo "email sung"
lsd datasets/Email-EuAll.txt -r complete -o results/eumail_sung.out --sung 
echo "email brankovic"
lsd datasets/Email-EuAll.txt -r complete -o results/eumail_brank.out --brankovic
echo "email sung brankovic"                 
lsd datasets/Email-EuAll.txt -r complete -o results/eumail_sung_brank.out --sung --brankovic

rm result.txt
for i in $( ls results/); do
     echo $i >> result.txt
     grep Elapsed results/$i|awk '{printf "%d\n", $5}'>> result.txt
done