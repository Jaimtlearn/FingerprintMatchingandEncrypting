import os
import cv2

sample = cv2.imread("fingerprints/proj/2__F_Left_middle_finger.BMP")
# sample = cv2.resize(sample, None, fx=4, fy=4)

database_path = "fingerprints/proj"

def MatchingFingerprint(sample,database_path):
    filename = None
    image = None
    best_score = 0
    kp1, kp2, mp = None, None, None

    sift = cv2.SIFT_create()
    keyp1, desc1 = sift.detectAndCompute(sample,None)
    for file in [file for file in os.listdir(database_path)]:
        fingerprint_image = cv2.imread(f"{database_path}/" + file)
        keyp2, desc2 = sift.detectAndCompute(fingerprint_image,None)

        matches = cv2.FlannBasedMatcher({'algorithm' : 1, 'trees' : 50}, {}).knnMatch(desc1,desc2, k=2)

        match_point = []
        for p, q in matches:
            if p.distance < 0.1* q.distance:
                match_point.append(p)

        keypoints = min(len(keyp1),len(keyp2))

        if len(match_point) / keypoints * 100 > best_score:
            best_score = len(match_point) / keypoints * 100
            filename = file
            image = fingerprint_image
            kp1,kp2,mp = keyp1,keyp2,match_point
    
    # print("Best Match " + filename)
    # print("score " + str(best_score))
    # result = cv2.drawMatches(sample,kp1,image,kp2,mp,None)
    # result = cv2.resize(result,None,fx=4,fy=4)
    # cv2.imshow("Result",result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return (filename, best_score, kp1, kp2, image, mp)


return_obj = MatchingFingerprint(sample=sample,database_path=database_path)
try:
    if return_obj[0] != None:
        print(f"Matched File Name : {return_obj[0]}")
        print(f"Accuracy : {return_obj[1]}")
    try:
        while True:
            inp = int(input("To see the result Enter 1, Enter 2 to break : "))
            if inp == 1:
                result = cv2.drawMatches(sample,return_obj[2],return_obj[4],return_obj[3],return_obj[5],None)
                result = cv2.resize(result,None,fx=4,fy=4)
                cv2.imshow("Result",result)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            elif inp == 2:
                break
            else:
                print("Please Enter different number")   
    except:
        print("Entered input is Not a number")


except:
    print("Error in the Input")


# cv2.imshow("Sample",sample)
# cv2.waitKey(0)
# cv2.destroyAllWindows()