echo Add a comment
read user_comment
steps=50
date=`date '+%Y-%m-%d %H:%M:%S'`
python3 train.py > test.txt \
  --bottleneck_dir=logs/bottlenecks \
  --how_many_training_steps=$steps \
  --training_percentage=80 \
  --validation_percentage=10 \
  --testing_percentage=10 \
  --model_dir=inception \
  --summaries_dir=logs/training_summaries/basic \
  --output_graph=logs/trained_graph.pb \
  --output_labels=logs/trained_labels.txt \
  --image_dir="/media/iza/UBUNTU 17_1/dataset"
echo "Date =" $date >> "logfile.txt"
echo "Steps =" $steps >> "logfile.txt"

cat test.txt | grep "Final" -A1 | head -n 1 >> "logfile.txt"
echo "Comment =" $user_comment >> "logfile.txt"
echo "" >> "logfile.txt"
rm test.txt
