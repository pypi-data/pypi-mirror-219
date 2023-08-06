import valueApi

def testSingleValue(myApiKey, myFieldId, myValue):
        print("Starting to add a single value.")
        valueApi.AddSingleValue(myApiKey, myFieldId, myValue)
        print("Done adding a single value.")

def testManyValues(myApiKey, myFieldId, myValues):
        print("Starting to add a batch of values.")
        result = valueApi.AddManyValues(myApiKey, myFieldId, myValues)
        print("status code: " + str(result.status_code))
        print("content: " + result.text)
        print("Done adding batch values.")

def testGetValues(myApiKey, myFieldId, myOffset, myLimit, myOrder):
        print("Starting to get values.")
        result = valueApi.GetValues(myApiKey, myFieldId, myOffset, myLimit, myOrder);
        print("status code: " + str(result.status_code))
        print("content: " + result.text)
        print("Done getting values.")

myApiKey = "pVUYgxZySwbp6iSvmQQLQHl0ywA2X3m5Gg93cKSFoMPU5k6IVTWgoUUV9YpsAQh0"
myFieldId = 2
myOffset = 0
myLimit = 10
myOrder = "asc"

myValues = [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20"
        ]

print("hello world\n")
#testSingleValue(myApiKey, myFieldId, myValues[2])
#testManyValues(myApiKey, myFieldId, myValues)
testGetValues(myApiKey, myFieldId, myOffset, myLimit, myOrder)