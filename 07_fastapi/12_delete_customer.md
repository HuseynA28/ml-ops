## Create new endpoint for delete
- mall.main.py
```
# Delete a customer by id
@app.delete("/customer/{id}", status_code=status.HTTP_200_OK)
async def delete_customer(id: int, session: Session = Depends(get_db)):
    with session:
        one_customer = session.get(Customer, id)
        if not one_customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Customer with {id} has not found.")
        session.delete(one_customer)
        session.commit()
        return {"ok": True}
```
## Browser
- http://127.0.0.1:8002/docs#/default/delete_customer_customer__id__delete
- Try some existing and non-existing customer ids
- Non-existing customer response
```commandline
{
  "detail": "Customer 5 has not found."
}
```

## Additional info
- If you don't want to return any response use Status Code 204 No Content. 
- It’s better to reduce traffic and simply tell the client the deletion is complete and return no response body (as the resource has been deleted).

### Is a response-body allowed for a HTTP-DELETE-request?
https://stackoverflow.com/questions/6581285/is-a-response-body-allowed-for-a-http-delete-request

### HTTP status code for update and delete?
https://stackoverflow.com/questions/2342579/http-status-code-for-update-and-delete

