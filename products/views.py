from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from .tasks import *
from background_task.models import Task
from rest_framework.views import APIView
from rest_framework import status

from django.http import JsonResponse

def custom_404_handler(request, exception=None):
    return JsonResponse(
        {"error": "Invalid API path. Please check the URL."},
        status=404
    )


@api_view(['GET'])
def trigger_background_tasks(request):
    update_products()
    update_orders()
    return Response({"message": "Background tasks scheduled successfully"})



@api_view(['DELETE'])
def terminate_task(request, task_name):
    """
    Terminates a scheduled background task by name if the task has not yet started executing.
    """
    tasks_deleted, _ = Task.objects.filter(task_name=task_name).delete()
    
    if tasks_deleted:
        return Response({"message": f"Task '{task_name}' terminated successfully."})
    else:
        return Response({"error": f"No pending task found with name '{task_name}'."}, status=404)


@api_view(['GET'])
def list_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def list_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

class StartRecurringTaskView(APIView):
    """
    API to start the recurring update_products task
    """

    def post(self, request):
        # update_products_recurring(repeat=600)  
        return Response({"message": "Recurring task scheduled successfully."}, status=status.HTTP_201_CREATED)


class ListRecurringTasksView(APIView):
    """
    API to list all scheduled recurring tasks
    """

    def get(self, request):
        tasks = Task.objects.filter(task_name="products.tasks.update_products_recurring")
        if tasks.exists():
            task_data = [{"task_name": task.task_name, "next_run": task.run_at} for task in tasks]
            return Response({"tasks": task_data}, status=status.HTTP_200_OK)
        return Response({"message": "No recurring tasks found."}, status=status.HTTP_404_NOT_FOUND)


class CancelRecurringTaskView(APIView):
    """
    API to cancel the update_products recurring task
    """

    def delete(self, request):
        Task.objects.filter(task_name="products.tasks.update_products_recurring").delete()
        return Response({"message": "Recurring task canceled successfully."}, status=status.HTTP_200_OK)
    
class ScheduleRecurringTaskView(APIView):
    """
    API to schedule a recurring update_products task with user-defined schedule and repeat interval.
    """

    def post(self, request):
        schedule_time = request.data.get("schedule", 60) 
        repeat_time = request.data.get("repeat", 600)  

        update_products_recurring_dynamic(schedule=schedule_time, repeat=repeat_time)

        return Response({
            "message": "Recurring task scheduled successfully.",
            "schedule_time": schedule_time,
            "repeat_time": repeat_time
        }, status=status.HTTP_201_CREATED)
    


# import React, { useState } from "react";

# const ScheduleTask = () => {
#     const [selectedDateTime, setSelectedDateTime] = useState("");

#     const calculateSchedule = () => {
#         if (!selectedDateTime) {
#             alert("Please select a date and time.");
#             return;
#         }

#         // Convert selected date-time to timestamp (milliseconds)
#         let selectedTimestamp = new Date(selectedDateTime).getTime();

#         // Get the current timestamp (milliseconds)
#         let currentTimestamp = new Date().getTime();

#         // Calculate difference in seconds
#         let scheduleInSeconds = Math.floor((selectedTimestamp - currentTimestamp) / 1000);

#         // Ensure schedule is not negative (past dates should be handled)
#         if (scheduleInSeconds < 0) {
#             alert("Please select a future date and time.");
#             return;
#         }

#         return scheduleInSeconds;
#     };

#     const handleSubmit = async () => {
#         let scheduleTime = calculateSchedule();
#         let repeatTime = 900; // Example: Repeat every 15 minutes

#         if (scheduleTime === undefined) return;

#         try {
#             let response = await fetch("http://127.0.0.1:8000/schedule-task/", {
#                 method: "POST",
#                 headers: {
#                     "Content-Type": "application/json",
#                 },
#                 body: JSON.stringify({
#                     schedule: scheduleTime,
#                     repeat: repeatTime,
#                 }),
#             });

#             let data = await response.json();
#             console.log("Response:", data);
#             alert("Task scheduled successfully!");
#         } catch (error) {
#             console.error("Error:", error);
#             alert("Failed to schedule task.");
#         }
#     };

#     return (
#         <div>
#             <h2>Schedule Recurring Task</h2>
#             <label>Select Date & Time:</label>
#             <input
#                 type="datetime-local"
#                 value={selectedDateTime}
#                 onChange={(e) => setSelectedDateTime(e.target.value)}
#             />
#             <button onClick={handleSubmit}>Schedule Task</button>
#         </div>
#     );
# };

# export default ScheduleTask;
