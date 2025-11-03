from fastapi.responses import JSONResponse

def success_response(data=None, message="", status_code=200):
	return JSONResponse(
		content={
			"success": True,
			"code": status_code,
			"message": message,
			"data": data},
		status_code=status_code
	)

def error_response(status_code=400, message=""):
	return JSONResponse(
		content={
			"success": True,
			"code": status_code,
			"message": message,
			"data": None},
		status_code=status_code
	)