"""LLM API 使用的成本估算工具。

本模块提供基于 token 计数来估算 LLM API 调用成本的函数。
成本估算基于 OpenAI 定价，对其他模型供应商可能有所不同。
"""

import logging

import tiktoken

logger = logging.getLogger(__name__)

# Per OpenAI Pricing Page: https://openai.com/api/pricing/
ENCODING_MODEL = "o200k_base"
INPUT_COST_PER_TOKEN = 0.000005
OUTPUT_COST_PER_TOKEN = 0.000015
IMAGE_INFERENCE_COST = 0.003825
EMBEDDING_COST = 0.02 / 1000000  # Assumes new ada-3-small


def estimate_llm_cost(input_content: str, output_content: str) -> float:
    """基于输入和输出内容估算 LLM API 调用的成本。

    成本估算基于 OpenAI 定价，对其他模型可能有所不同。

    Args:
        input_content: 发送给 LLM 的输入文本。
        output_content: 从 LLM 接收的输出文本。

    Returns:
        估算的成本（美元）。失败时返回 0。
    """
    try:
        encoding = tiktoken.get_encoding(ENCODING_MODEL)
        input_tokens = encoding.encode(input_content)
        output_tokens = encoding.encode(output_content)
        input_costs = len(input_tokens) * INPUT_COST_PER_TOKEN
        output_costs = len(output_tokens) * OUTPUT_COST_PER_TOKEN
        return input_costs + output_costs
    except Exception as e:
        logger.warning(
            f"成本估算失败（tiktoken 编码文件可能未下载），跳过成本计算: {type(e).__name__}: {e}"
        )
        return 0.0


def estimate_embedding_cost(model: str, docs: list) -> float:
    """估算嵌入文档的成本。

    Args:
        model: 嵌入模型的名称。
        docs: 要嵌入的文档列表。

    Returns:
        估算的嵌入成本（美元）。失败时返回 0。
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
        total_tokens = sum(len(encoding.encode(str(doc))) for doc in docs)
        return total_tokens * EMBEDDING_COST
    except Exception as e:
        logger.warning(
            f"嵌入成本估算失败，跳过成本计算: {type(e).__name__}: {e}"
        )
        return 0.0

