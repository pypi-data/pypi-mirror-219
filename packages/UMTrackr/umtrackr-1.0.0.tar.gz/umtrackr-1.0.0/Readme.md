# Instructions
### Step 1:
Add import statement to top of python file
## Step 3:
Use Trackr functions within your own code. 



# Example working cs file
import Trackr

def testUpdateEndpoint(myUrl):<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print("Current endpoint is " + Trackr.ShowEndpoint())<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Trackr.UpdateEndpoint(myUrl)<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print("New endpoint is " + Trackr.ShowEndpoint())<br>

def testManyValues(myApiKey, myFieldId: int, values):<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print("adding many values")<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;response = Trackr.AddManyValues(myApiKey, myFieldId, values)<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print("Returned status code: " + str(response.status_code))<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print("Returned content: " + str(response.text))<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print("done adding many values")<br>

def testSingleValue(myApiKey, myFieldId: int, value):<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print("adding single value")<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;response = Trackr.AddSingleValue(myApiKey, myFieldId, value)<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print("Returned status code: " + str(response.status_code))<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print("Returned content: " + str(response.text))<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print("done adding single value")<br>

def testGetValues(myApiKey, myFieldId: int, myOffset: int, myLimit: int, myOrder):<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print("getting values")<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;returnedValues = Trackr.GetValues(myApiKey, myFieldId, myOffset, myLimit, myOrder)<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print(returnedValues)<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print("done getting values")<br>

myApiKey = "pVUYgxZySwbp6iSvmQQLQHl0ywA2X3m5Gg93cKSFoMPU5k6IVTWgoUUV9YpsAQh0"<br>
myFieldId = 1<br>
myOffset = 0<br>
myLimit = 10<br>
myOrder = "asc"<br>
myUrl = "someAddress/api/values"<br>

myValues = [<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"1",<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"2",<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"3",<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"4",<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"5",<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"6",<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"7"<br>
]<br>

testManyValues(myApiKey, myFieldId, myValues)<br>
print("")<br>
testSingleValue(myApiKey, myFieldId, myValues[0])<br>
print("")<br>
testGetValues(myApiKey, myFieldId, myOffset, myLimit, myOrder)<br>
print("")<br>
testUpdateEndpoint(myUrl)<br>