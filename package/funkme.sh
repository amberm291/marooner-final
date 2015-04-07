python edgeDetect.py $1
echo "->canny edge on user image performed..."
python boxcalc.py canny.png > boxDim
echo "->surronding box calculated on canny edge user image..."
python removeBlackPix.py $1
echo "->complete black pixels removed from user image..."
cat boxDim maxiters > grabcutInput
echo "->input compilation for grabcut done..."
python grabcutauto.py blackPixRemoved.png < grabcutInput
echo "->grabcut performed on user image with removed black pixels and using calculated box dimensions..."
echo "->now we must have got our shirt/tshirt extracted..."
python removeTurds.py output.png
echo "->small turds removed from extracted shirt/tshirt image..."
python cropImg.py mainOutput.png > origin
echo "->shirt/tshirt image cropped..."
python removeBlackPix.py $2
echo "->black pixels removed from cropped image..."
python discretize.py blackPixRemoved.png 2
echo "->catalogue image discretized into 2 divisions..."
python flood.py discretized.png blackPixRemoved.png
echo "->catalogue image background made black..."
python cropImg.py floodout.png > garbage
echo "->catalogue image cropped..."
python resizeSameUser.py croppedmainOutput.png croppedfloodout.png
echo "->cropped catalogue image resized to user image for sleeve fitting..."
python calcResize.py croppedmainOutput.png resizedSameUsercroppedfloodout.png > resize
echo "->resizing calculations done..."
python resizeIntoUser.py croppedmainOutput.png croppedfloodout.png < resize
echo "->cropped catalogue image resized to 1.1 times user cropped image for central body fitting..."
python 3segappr.py resizedSameUsercroppedfloodout.png > segLines
echo "->left and right vertical lines detected for sleeve fitting..."
python fitver5.py croppedmainOutput.png resizedcroppedfloodout.png
echo "->center-to-away fitting performed on central body portion..."
python armPitLine.py croppedmainOutput.png > armPitLine
echo "->armpit horizontal line detected in user image..."
cat segLines armPitLine > fittingInput
echo "->input compilation..."
python 3segfit.py resultfitver5.png resizedSameUsercroppedfloodout.png < fittingInput
echo "->sleeve fitting performed..."
cat fittingInput medianWindowSize > blurInput
echo "->median blur input compilation..."
python medianFilter.py result3seg.png < blurInput
echo "->median blur peroformed performed..."
python medianFilterComplete.py result3seg.png < blurInput
echo "->Complete median blur peroformed performed..."
python fittingOntoUser.py $1 medianFiltered.png < origin > outFileName
echo "->final output compilation with partial median filter done..."
sleep 1
python fittingOntoUser.py $1 medianFilteredComplete.png < origin > outFileName2
echo "->final output compilation with complete median filter done..."
outFile=`cat outFileName`
outFile2=`cat outFileName2`
mkdir debug
mkdir finalOutputs
mv box.png debug/
mv armPitLine.png debug/
mv armPitLine debug/
mv blackPixRemoved.png debug/
mv boxDim debug/
mv canny.png debug/
mv croppedfloodout.png debug/
mv croppedmainOutput.png debug/
mv mainOutput.png debug/
mv resizedcroppedfloodout.png debug/
mv resizedSameUsercroppedfloodout.png debug/
mv output.png debug/
mv result3seg.png debug/
mv resultfitver5.png debug/
mv floodout.png debug/
mv discretized.png debug/
mv $outFile finalOutputs/
mv $outFile2 finalOutputs/
mv fittingInput debug/
mv resize debug/
mv segLines debug/
mv origin debug/
mv blurInput debug/
mv medianFiltered.png debug/
mv medianFilteredComplete.png debug/
mv segments1resizedSameUsercroppedfloodout.png debug/
rm garbage
rm outFileName
rm outFileName2