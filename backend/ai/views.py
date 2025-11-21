import json

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AiLog
from .serializers import AiLogSerializer
from .services import AIService


class AIInstructionView(APIView):
    @staticmethod
    def _extract_instruction(request):
        instruction = request.data.get("instruction")
        if instruction:
            return instruction

        query_instruction = request.query_params.get("instruction")
        if query_instruction:
            return query_instruction

        raw_body = request.body.decode("utf-8").strip() if request.body else ""
        if not raw_body:
            return ""

        if raw_body.startswith("{"):
            try:
                parsed = json.loads(raw_body)
                return parsed.get("instruction", "")
            except json.JSONDecodeError:
                return ""

        return raw_body

    def post(self, request):
        instruction = self._extract_instruction(request)
        if not instruction or not instruction.strip():
            return Response(
                {"detail": "instruction is required (send JSON {\"instruction\": \"...\"} or raw text)"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        service = AIService()
        try:
            result = service.process_instruction(instruction.strip())
            return Response(result, status=status.HTTP_201_CREATED)
        except Exception as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)


class AiLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AiLog.objects.all()
    serializer_class = AiLogSerializer
