#rm -f debug/*
if [ $4 -eq 0 ]
then
	python grabcut.py $1
	##echo "->grabcut performed on user image with removed black pixels and using calculated box dimensions..."
	##echo "->now we must have got our shirt/tshirt extracted..."
	#echo "->removeTurds"
	python removeTurds.py grabcutOutput.png
	#echo "->cropImg USER"
	python cropImg.py turdsOut.png > origin
else
	cp $5 croppedturdsOut.png
	cp $6 origin
fi

#echo "->colorUser"
time python colorUser.py croppedturdsOut.png $2

#echo "->removeBlackPix"
python removeBlackPix.py $2
##echo "->black pixels removed from cropped image..."
if [ $3 -eq 2 ]
then
	#echo "->edgeDetect2"
	python edgeDetect2.py $2
else
	#echo "None"
	#echo "->dicretize"
	python discretize.py $2 16 $3
	python flood.py discretized.png $2
	python removeTurds.py floodOut.png
	mv turdsOut.png floodOut.png
	##echo "->catalogue image discretized into 2 divisions..."
fi


#echo "->flood"

#echo "->cropImg CATALOGUE"
python cropImg.py floodOut.png > garbage
#echo "->resizeSameUser"
python resizeSameUser.py colorUserOut.png croppedfloodOut.png
#echo "->calcResize"
python calcResize.py colorUserOut.png resizedSameUserOut.png > resize
#echo "->resizeIntoUser"
python resizeIntoUser.py colorUserOut.png croppedfloodOut.png < resize
#echo "->3segappr USER"
python 3segappr.py colorUserOut.png > segLines
#echo "->3segappr PRODUCT"
python 3segappr.py resizedcroppedfloodOut.png > segLines2
##echo "->left and right vertical lines detected PRODUCT..."
#python edgeDetect2.py resizedcroppedfloodOut.png 
#cp floodOut.png resizedcroppedfloodOut.png
cat segLines segLines2 > segLinesIn
#echo "fitver5"
python armSegment.py colorUserOut.png resizedcroppedfloodOut.png < segLinesIn
python armsRemTurds.py leftUser.png
python armsRemTurds.py rightUser.png
python armsRemTurds.py leftProduct.png
python armsRemTurds.py rightProduct.png

python armRotate3.py turdsRemleftUser.png turdsRemrightUser.png turdsRemleftProduct.png turdsRemrightProduct.png
#python edgeDetect2.py finalrotateright.png
#cp floodOut.png finalrotateright.png
#python edgeDetect2.py finalrotateleft.png
#cp floodOut.png finalrotateleft.png
python fitver2.py colorUserOut.png resizedcroppedfloodOut.png > garbage < segLinesIn

python 3segver3.py resultfitver5.png finalrotateleft.png finalrotateright.png
#echo "->armPitLine"
python armPitLine.py colorUserOut.png > armPitLine
##echo "->armpit horizontal line detected in user image..."
cat segLines armPitLine > fittingInput
#echo "->3segver2"
#python 3segver2.py resultfitver5.png resizedSameUserOut.png < fittingInput
#python 3segver2.py resultfitver5.png resizedSameUserOut.png < segLinesIn
##echo "->sleeve fitting performed..."
#cat fittingInput medianWindowSize > blurInput
##echo "->median blur input compilation..."
#python medianFilter.py result3seg.png < blurInput
##echo "->median blur peroformed performed..."
#python medianFilterComplete.py result3seg.png < blurInput
##echo "->Complete median blur peroformed performed..."
#echo "->fittingOntoUser"
python fittingOntoUser.py $1 resultfitver5.png $2 < origin > outFileName
##echo "->final output compilation with partial median filter done..."
#python fittingOntoUser.py $1 result3seg.png < origin > outFileName2
##echo "->final output compilation with complete median filter done..."
outFile=`cat outFileName`
#outFile2=`cat outFileName2`
#mkdir debug
#mkdir finalOutputs
mv armPitLine debug/
#mv boxDim debug/
mv $outFile finalOutputs/
#mv $outFile2 finalOutputs/
mv fittingInput debug/
mv resize debug/
mv segLines debug/
mv origin debug/
#mv blurInput debug/
mv *.png debug/
#rm garbage
rm outFileName
#rm outFileName2